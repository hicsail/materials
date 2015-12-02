import re
from db import Listing, Property, Measurement, Reference, Component, Mixture
from db import get_or_create


class NistParser:
    def __init__(self, session, data, url):
        self.session = session
        self.data = data
        self.url = url

    def parse_and_store(self):
        # Components
        components, component_mixtures = self._parse_components()
        # Reference
        reference = self._parse_reference()
        # Mixture
        mixture = self._parse_mixture(components, component_mixtures)
        # Listing
        listing, listing_created = self._parse_listing(mixture, reference)
        # Properties
        properties = self._parse_properties()
        # Measurements
        self._parse_measurements(listing, listing_created, properties)

        self.session.commit()

    def _parse_components(self):
        components = []
        component_mixtures = []
        for i in xrange(len(self.data['components'])):
            component, created = get_or_create(self.session, Component, name=self.data['components'][i]['name'])
            if created:
                component.formula = self.data['components'][i]['formula']
                # We need the component IDs, don't know what they are before adding to the db
                self.session.commit()
            # Store components in case we have to add a mixture later on
            components.append(component)
            # Build list of mixture IDs for each component
            component_mixtures.append([x.id for x in component.mixtures])
        return components, component_mixtures

    def _parse_reference(self):
        reference, created = get_or_create(self.session, Reference, full=self.data['ref']['full'])
        if created:
            reference.title = self.data['ref']['title']
        return reference

    def _parse_mixture(self, components, component_mixtures):
        # See if components already share a mixture, should only ever be one mixture
        shared_mixture = set(component_mixtures[0]).intersection(*component_mixtures[:1])
        if shared_mixture:
            mix_id = shared_mixture.pop()
            mixture = self.session.query(Mixture).filter(Mixture.id == mix_id).first()
        else:
            mixture = Mixture()
            # New mixture, add it to the existing components
            for comp in components:
                comp.mixtures.append(mixture)
        return mixture

    def _parse_listing(self, mixture, reference):
        listing, listing_created = get_or_create(self.session, Listing, url=self.url, reference=reference,
                                                 mixture=mixture)
        mixture.listings.append(listing)
        return listing, listing_created

    def _parse_properties(self):
        properties = []
        for i in xrange(len(self.data['dhead'])):
            term = self.data['dhead'][i][0]
            # Properties have two possible forms, with and without a unit
            # The unit is the last part after "comma space" in the string, e.g "Temperature, K"
            # Properties like Refractive index do not have a unit
            # This regex splits up the property into everything before and after the last "comma space" occurrence
            parts = re.search('(.*),\s(.*)', term)
            try:
                prop_name = parts.group(1)
                unit = parts.group(2)
                # Replace black small circle with UTF-8 middle dot for multiplication symbol
                unit = unit.replace('&#8226;', u'\u00B7')
            except AttributeError:
                # If no unit is found, the property is considered to be the full string
                prop_name = term
                unit = None
            # Add properties to self.database or get existing one
            prop, created = get_or_create(self.session, Property, name=prop_name, unit=unit)
            # Make sure we have the property ID if these are new properties
            self.session.commit()
            # Store the ID to use in measurement
            properties.append(prop.id)
        return properties

    def _parse_measurements(self, listing, listing_created, properties):
        # Only proceed if we created a new listing, otherwise measurements would be duplicated
        if listing_created:
            # Get the last measurement group ID and increment by 1
            measurement_group_id = self.session.query(Measurement.measurement_group_id) \
                .order_by(Measurement.measurement_group_id.desc()).first()
            if measurement_group_id:
                # Result is a tuple with one element
                measurement_group_id = measurement_group_id[0] + 1
            else:
                measurement_group_id = 1

            for measurement_group in self.data['data']:
                measurements = []
                # Use i to be able to access properties[i] since this matches the order of the individual measurements
                for i in xrange(len(measurement_group)):
                    # TODO check if temp, pressure and ref already existing and add to that??
                    try:
                        m = Measurement(error=measurement_group[i][1], value=measurement_group[i][0],
                                        listing_id=listing.id,
                                        property_id=properties[i], measurement_group_id=measurement_group_id)
                    except IndexError:
                        # No error property is present, try again without it
                        m = Measurement(value=measurement_group[i][0], listing_id=listing.id,
                                        property_id=properties[i], measurement_group_id=measurement_group_id)
                    measurements.append(m)

                self.session.add_all(measurements)
                measurement_group_id += 1
