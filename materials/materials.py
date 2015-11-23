import sqlalchemy
import json
import re
from config import config
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from db import Base, Listing, Property, Measurement, Reference, Component, Mixture


def init():
    print sqlalchemy.__version__
    engine = engine_from_config(config, prefix='sqlalchemy.')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    data = json.loads(
        '{"data":[[["293.15"],["0"],["101"],["0.00272","2e-05"]],[["293.15"],["0.05"],["101"],["0.00365","3e-05"]],[["293.15"],["0.11"],["101"],["0.00471","5e-05"]],[["293.15"],["0.16"],["101"],["0.00605","6e-05"]],[["293.15"],["0.21"],["101"],["0.00777","7e-05"]],[["293.15"],["0.26"],["101"],["0.00988","8e-05"]],[["293.15"],["0.32"],["101"],["0.01236","0.00011"]],[["293.15"],["0.37"],["101"],["0.01513","0.00013"]],[["293.15"],["0.42"],["101"],["0.01811","0.00016"]],[["293.15"],["0.47"],["101"],["0.02123","0.00018"]],[["293.15"],["0.53"],["101"],["0.02442","0.00023"]],[["293.15"],["0.58"],["101"],["0.02769","0.00025"]],[["293.15"],["0.63"],["101"],["0.0311","0.00029"]],[["293.15"],["0.68"],["101"],["0.03477","0.00033"]],[["293.15"],["0.74"],["101"],["0.03897","0.00039"]],[["293.15"],["0.79"],["101"],["0.04405","0.00044"]],[["293.15"],["0.84"],["101"],["0.05053","0.00045"]],[["293.15"],["0.89"],["101"],["0.05909","0.00056"]],[["293.15"],["0.95"],["101"],["0.07058","0.00088"]],[["293.15"],["1"],["101"],["0.0861","0.0013"]],[["298.15"],["0"],["101"],["0.00252","2e-05"]],[["298.15"],["0.05"],["101"],["0.00326","3e-05"]],[["298.15"],["0.11"],["101"],["0.00414","4e-05"]],[["298.15"],["0.16"],["101"],["0.00529","5e-05"]],[["298.15"],["0.21"],["101"],["0.00674","6e-05"]],[["298.15"],["0.26"],["101"],["0.00851","8e-05"]],[["298.15"],["0.32"],["101"],["0.01056","9e-05"]],[["298.15"],["0.37"],["101"],["0.01282","0.00012"]],[["298.15"],["0.42"],["101"],["0.01523","0.00014"]],[["298.15"],["0.47"],["101"],["0.01772","0.00017"]],[["298.15"],["0.53"],["101"],["0.02025","0.00019"]],[["298.15"],["0.58"],["101"],["0.02281","0.00022"]],[["298.15"],["0.63"],["101"],["0.02545","0.00025"]],[["298.15"],["0.68"],["101"],["0.02828","0.00028"]],[["298.15"],["0.74"],["101"],["0.03151","0.00032"]],[["298.15"],["0.79"],["101"],["0.03542","0.00036"]],[["298.15"],["0.84"],["101"],["0.04044","0.00042"]],[["298.15"],["0.89"],["101"],["0.04709","0.0005"]],[["298.15"],["0.95"],["101"],["0.05605","0.00055"]],[["298.15"],["1"],["101"],["0.06816","0.00081"]],[["303.15"],["0"],["101"],["0.00229","2e-05"]],[["303.15"],["0.05"],["101"],["0.00293","3e-05"]],[["303.15"],["0.11"],["101"],["0.0037","3e-05"]],[["303.15"],["0.16"],["101"],["0.00468","4e-05"]],[["303.15"],["0.21"],["101"],["0.0059","5e-05"]],[["303.15"],["0.26"],["101"],["0.00736","6e-05"]],[["303.15"],["0.32"],["101"],["0.00903","8e-05"]],[["303.15"],["0.37"],["101"],["0.01087","0.0001"]],[["303.15"],["0.42"],["101"],["0.01283","0.00012"]],[["303.15"],["0.47"],["101"],["0.01485","0.00014"]],[["303.15"],["0.53"],["101"],["0.01691","0.00016"]],[["303.15"],["0.58"],["101"],["0.019","0.00018"]],[["303.15"],["0.63"],["101"],["0.02115","0.0002"]],[["303.15"],["0.68"],["101"],["0.02345","0.00022"]],[["303.15"],["0.74"],["101"],["0.02604","0.00025"]],[["303.15"],["0.79"],["101"],["0.02914","0.00028"]],[["303.15"],["0.84"],["101"],["0.03305","0.00033"]],[["303.15"],["0.89"],["101"],["0.03815","0.00038"]],[["303.15"],["0.95"],["101"],["0.04495","0.00046"]],[["303.15"],["1"],["101"],["0.05405","0.0005"]],[["308.15"],["0"],["101"],["0.00214","2e-05"]],[["308.15"],["0.05"],["101"],["0.00268","2e-05"]],[["308.15"],["0.11"],["101"],["0.00334","3e-05"]],[["308.15"],["0.16"],["101"],["0.00417","4e-05"]],[["308.15"],["0.21"],["101"],["0.0052","5e-05"]],[["308.15"],["0.26"],["101"],["0.00644","6e-05"]],[["308.15"],["0.32"],["101"],["0.00785","7e-05"]],[["308.15"],["0.37"],["101"],["0.00939","8e-05"]],[["308.15"],["0.42"],["101"],["0.01101","0.0001"]],[["308.15"],["0.47"],["101"],["0.01268","0.00011"]],[["308.15"],["0.53"],["101"],["0.01435","0.00013"]],[["308.15"],["0.58"],["101"],["0.01604","0.00014"]],[["308.15"],["0.63"],["101"],["0.01776","0.00016"]],[["308.15"],["0.68"],["101"],["0.01959","0.00018"]],[["308.15"],["0.74"],["101"],["0.02164","0.0002"]],[["308.15"],["0.79"],["101"],["0.02411","0.00023"]],[["308.15"],["0.84"],["101"],["0.02723","0.00026"]],[["308.15"],["0.89"],["101"],["0.03136","0.00031"]],[["308.15"],["0.95"],["101"],["0.0369","0.00037"]],[["308.15"],["1"],["101"],["0.04438","0.00045"]],[["313.15"],["0"],["101"],["0.002","2e-05"]],[["313.15"],["0.05"],["101"],["0.00245","2e-05"]],[["313.15"],["0.11"],["101"],["0.00302","3e-05"]],[["313.15"],["0.16"],["101"],["0.00375","3e-05"]],[["313.15"],["0.21"],["101"],["0.00464","4e-05"]],[["313.15"],["0.26"],["101"],["0.00569","5e-05"]],[["313.15"],["0.32"],["101"],["0.00687","6e-05"]],[["313.15"],["0.37"],["101"],["0.00815","7e-05"]],[["313.15"],["0.42"],["101"],["0.0095","8e-05"]],[["313.15"],["0.47"],["101"],["0.01088","9e-05"]],[["313.15"],["0.53"],["101"],["0.01228","0.00011"]],[["313.15"],["0.58"],["101"],["0.01368","0.00012"]],[["313.15"],["0.63"],["101"],["0.01511","0.00013"]],[["313.15"],["0.68"],["101"],["0.01662","0.00015"]],[["313.15"],["0.74"],["101"],["0.01829","0.00016"]],[["313.15"],["0.79"],["101"],["0.02027","0.00018"]],[["313.15"],["0.84"],["101"],["0.02274","0.00021"]],[["313.15"],["0.89"],["101"],["0.02592","0.00025"]],[["313.15"],["0.95"],["101"],["0.03014","0.00029"]],[["313.15"],["1"],["101"],["0.03576","0.00036"]],[["318.15"],["0"],["101"],["0.00185","2e-05"]],[["318.15"],["0.05"],["101"],["0.00226","2e-05"]],[["318.15"],["0.11"],["101"],["0.00277","2e-05"]],[["318.15"],["0.16"],["101"],["0.00339","3e-05"]],[["318.15"],["0.21"],["101"],["0.00416","4e-05"]],[["318.15"],["0.26"],["101"],["0.00505","5e-05"]],[["318.15"],["0.32"],["101"],["0.00606","5e-05"]],[["318.15"],["0.37"],["101"],["0.00716","6e-05"]],[["318.15"],["0.42"],["101"],["0.0083","7e-05"]],[["318.15"],["0.47"],["101"],["0.00947","9e-05"]],[["318.15"],["0.53"],["101"],["0.01064","9e-05"]],[["318.15"],["0.58"],["101"],["0.01181","0.00011"]],[["318.15"],["0.63"],["101"],["0.01299","0.00012"]],[["318.15"],["0.68"],["101"],["0.01422","0.00013"]],[["318.15"],["0.74"],["101"],["0.01558","0.00014"]],[["318.15"],["0.79"],["101"],["0.01718","0.00016"]],[["318.15"],["0.84"],["101"],["0.01916","0.00018"]],[["318.15"],["0.89"],["101"],["0.02173","0.00021"]],[["318.15"],["0.95"],["101"],["0.02514","0.00023"]],[["318.15"],["1"],["101"],["0.02972","0.0003"]]],"title":"Transport properties: Viscosity","dhead":[["Temperature, K",null],["Mole fraction of 1-butyl-1-methylpyrrolidinium bis[(trifluoromethyl)sulfonyl]imide","Liquid"],["Pressure, kPa",null],["Viscosity, Pa&#8226;s","Liquid"]],"ref":{"title":"Effect of Temperature and Composition on the Transport  and Thermodynamic Properties of Binary Mixtures  of Ionic Liquid N-Butyl-N-methylpyrrolidinium  bis(Trifluoromethanesulfonyl)imide and Propylene  Carbonate","full":"Zarrougui, R.; Dhahbi, M.; Lemordant, D. (2010) J. Solution Chem. 39, 921-942."},"constr":[],"expmeth":"Capillary tube (Ostwald; Ubbelohde) method","solvent":null,"components":[{"name":"1,2-propanediyl carbonate","idout":"AATgpU","sample":[["Source:","commercial source"],["Purification:","stated by supplier"],["Purity:","99.7 % (basis not specified)"],["Purity analysis:","fractional distillation"]],"mw":"102.09","formula":"C<SUB>4</SUB>H<SUB>6</SUB>O<SUB>3</SUB>"},{"mw":"422.41","sample":[["Source:","commercial source"],["Initial purification:","stated by supplier"],["Initial purity:","99.5 % (basis not specified)"],["Final purification:","ion-selective electrode;Karl Fischer titration"],["Final purity:","0.0005 halide impurity mass %;0.005 water mass %(molecular sieve treatment)"]],"idout":"ABdMdV","name":"1-butyl-1-methylpyrrolidinium bis[(trifluoromethyl)sulfonyl]imide","formula":"C<SUB>11</SUB>H<SUB>20</SUB>F<SUB>6</SUB>N<SUB>2</SUB>O<SUB>4</SUB>S<SUB>2</SUB>"}],"phases":["Liquid"],"footer":""}')
    parse_string(Session, data)


def parse_string(Session, data):
    session = Session()
    # Components
    components = []
    component_mixtures = []
    for i in xrange(len(data['components'])):
        component, created = get_or_create(session, Component, name=data['components'][i]['name'])
        if created:
            component.formula = data['components'][i]['formula']
            # We need the component IDs, don't know what they are before adding to the db
            session.commit()
        # Store components in case we have to add a mixture later on
        components.append(component)
        # Build list of mixture IDs for each component
        component_mixtures.append([x.id for x in component.mixtures])

    # Reference
    reference, created = get_or_create(session, Reference, full=data['ref']['full'])
    if created:
        reference.title = data['ref']['title']

    # Mixture
    # See if components already share a mixture, should only ever be one mixture
    shared_mixture = set(component_mixtures[0]).intersection(*component_mixtures[:1])
    if shared_mixture:
        mix_id = shared_mixture.pop()
        mixture = session.query(Mixture).filter(Mixture.id == mix_id).first()
    else:
        mixture = Mixture()
        # New mixture, add it to the existing components
        for comp in components:
            comp.mixtures.append(mixture)

    # Listing
    # TODO fix url
    listing, listing_created = get_or_create(session, Listing, url='test', reference=reference, mixture=mixture)
    mixture.listings.append(listing)

    # Properties
    properties = []
    for i in xrange(len(data['dhead'])):
        prop_name, unit = None, None
        term = data['dhead'][i][0]
        # Search for word after comma space
        # Unit is searched first since the property search returns everything before a comma, even if it isn't there
        try:
            unit = re.search('(?:,\s)(.*)$', term).group(1)
            # Replace black small circle with UTF-8 middle dot for multiplication symbol
            unit = unit.replace('&#8226;', u'\u00B7')
        except AttributeError:
            # No need to do anything if no unit is found
            pass
        if unit:
            # Molality is of form: MolaLity of x, mol/kg. We want to drop the 'of x' part
            if "MolaLity" in unit:
                prop_name = "Molality"
            else:
                # All terms before potential comma
                prop_name = re.search('[^,]*', term).group(0)
        else:
            # First two words
            prop_name = re.search('(?:\w+\s)(?:\w+)', term).group(0)
        # Add properties to database or get existing one
        prop, created = get_or_create(session, Property, name=prop_name, unit=unit)
        # Make sure we have the property ID if these are new properties
        session.commit()
        # Store the ID to use in measurement
        properties.append(prop.id)

    # Measurements
    # Only proceed if we created a new listing, otherwise measurements would be duplicated
    if listing_created:
        # Get the last measurement group ID and increment by 1
        measurement_group_id = session.query(Measurement, Measurement.measurement_group_id) \
            .order_by(Measurement.measurement_group_id.desc()).first()
        if measurement_group_id:
            measurement_group_id += 1
        else:
            measurement_group_id = 1

        for measurement_group in data['data']:
            measurements = []
            # Use i to be able to access properties[i] since this matches the order of the individual measurements
            for i in xrange(len(measurement_group)):
                # TODO check if temp, pressure and ref already existing and add to that??
                try:
                    m = Measurement(error=measurement_group[i][1], value=measurement_group[i][0], listing_id=listing.id,
                                    property_id=properties[i], measurement_group_id=measurement_group_id)
                except IndexError:
                    # No error property is present, try again without it
                    m = Measurement(value=measurement_group[i][0], listing_id=listing.id,
                                    property_id=properties[i], measurement_group_id=measurement_group_id)
                measurements.append(m)

            session.add_all(measurements)
            measurement_group_id += 1

    session.commit()


# https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


if __name__ == '__main__':
    init()
