import os
import unittest

from entitypedia.query import QueryBuilder
from entitypedia.api import SparqlAPI
from entitypedia.coordinator import Coordinator
from entitypedia.saver import CSVSaver

BASE = os.path.join(os.path.dirname(__file__), '../data/sparql')


class TestCoordinator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/raw/seeds/')
        cls.coordinator = Coordinator(query_generator=QueryBuilder(),
                                      api=SparqlAPI(),
                                      saver=CSVSaver())

    def execute(self, dirname):
        template_dir = os.path.join(BASE, dirname)
        save_file = os.path.join(self.BASE_DIR, dirname + '.csv')
        if os.path.exists(save_file):
            os.remove(save_file)

        template_files = os.listdir(template_dir)
        for template_file in template_files:
            print(template_file)
            template_file = os.path.join(dirname, template_file)
            self.coordinator.execute(template_file=template_file,
                                     save_file=save_file)


class Name(TestCoordinator):

    def test_name_other(self):
        pass

    def test_person(self):
        pass

    def test_god(self):
        self.execute('name/god')


class Organization(TestCoordinator):

    """
    def test_organizaton_other(self):
        self.execute('organization/organizaton_other')

    def test_international_organization(self):
        self.execute('organization/international_organization')

    def test_show_organization(self):
        self.execute('organization/show_organization')

    def test_family(self):
        self.execute('organization/family')

    def test_ethnic_group_other(self):
        self.execute('organization/ethnic_group/ethnic_group_other')

    def test_nationality(self):
        self.execute('organization/ethnic_group/nationality')

    def test_sports_organization_other(self):
        self.execute('organization/sports_organization/sports_organization_other')

    def test_pro_sports_organization(self):
        self.execute('organization/sports_organization/pro_sports_organization')

    def test_sports_league(self):
        self.execute('organization/sports_organization/sports_league')

    def test_corporation_other(self):
        self.execute('organization/corporation/corporation_other')

    def test_compnay_group(self):
        self.execute('organization/corporation/compnay_group')
    """

    def test_company(self):
        self.execute('organization/corporation/company')

    def test_political_party(self):
        self.execute('organization/political_organization/political_party')

    def test_cabinet(self):
        self.execute('organization/political_organization/cabinet')

    def test_military(self):
        self.execute('organization/political_organization/military')

    def test_government(self):
        self.execute('organization/political_organization/government')

    def test_political_organization_other(self):
        self.execute('organization/political_organization/political_organization_other')


class Location(TestCoordinator):

    def test_spa(self):
        self.execute('location/spa')

    def test_city(self):
        self.execute('location/gpe/city')

    def test_county(self):
        self.execute('location/gpe/county')

    def test_province(self):
        self.execute('location/gpe/province')

    def test_country(self):
        self.execute('location/gpe/country')

    def test_continental_region(self):
        self.execute('location/region/continental_region')

    def test_domestic_region(self):
        self.execute('location/region/domestic_region')

    def test_mountain(self):
        self.execute('location/geological_region/mountain')

    def test_island(self):
        self.execute('location/geological_region/island')

    def test_river(self):
        self.execute('location/geological_region/river')

    def test_lake(self):
        self.execute('location/geological_region/lake')

    def test_sea(self):
        self.execute('location/geological_region/sea')

    def test_bay(self):
        self.execute('location/geological_region/bay')

    def test_astral_body_other(self):
        self.execute('location/astral_body/astral_body_other')

    def test_planet(self):
        self.execute('location/astral_body/planet')

    def test_star(self):
        self.execute('location/astral_body/star')

    def test_constellation(self):
        self.execute('location/astral_body/constellation')


class Facility(TestCoordinator):

    def test_archaeological_place_other(self):
        self.execute('facility/archaeological_place/archaeological_place_other')

    def test_tumulus(self):
        self.execute('facility/archaeological_place/tumulus')

    def test_public_institution(self):
        self.execute('facility/goe/public_institution')

    def test_school(self):
        self.execute('facility/goe/school')

    def test_research_institute(self):
        self.execute('facility/goe/research_institute')

    def test_market(self):
        self.execute('facility/goe/market')

    def test_park(self):
        self.execute('facility/goe/park')

    def test_sports_facility(self):
        self.execute('facility/goe/sports_facility')

    def test_museum(self):
        self.execute('facility/goe/museum')

    def test_zoo(self):
        self.execute('facility/goe/zoo')

    def test_amusement_park(self):
        self.execute('facility/goe/amusement_park')

    def test_theater(self):
        self.execute('facility/goe/theater')

    def test_worship_place(self):
        self.execute('facility/goe/worship_place')

    def test_car_stop(self):
        self.execute('facility/goe/car_stop')

    def test_station(self):
        self.execute('facility/goe/station')

    def test_airport(self):
        self.execute('facility/goe/airport')

    def test_port(self):
        self.execute('facility/goe/port')

    def test_railroad(self):
        self.execute('facility/line/railroad')

    def test_road(self):
        self.execute('facility/line/road')

    def test_canal(self):
        self.execute('facility/line/canal')

    def test_tunnel(self):
        self.execute('facility/line/tunnel')

    def test_bridge(self):
        self.execute('facility/line/bridge')


class Product(TestCoordinator):

    def test_offense(self):
        self.execute('product/offense')

    def test_newspaper(self):
        self.execute('product/printing/newspaper')

    def test_religion(self):
        self.execute('product/doctrine_method/religion')

    def test_national_language(self):
        self.execute('product/language/national_language')

    def test_currency(self):
        self.execute('product/unit/currency')


class Event(TestCoordinator):

    def test_war(self):
        self.execute('event/incident/war')

    def test_earthquake(self):
        self.execute('event/natural_phenomenon/earthquake')


class NaturalObject(TestCoordinator):

    def test_element(self):
        self.execute('natural_object/element')

    def test_compound(self):
        self.execute('natural_object/compound')

    def test_mineral(self):
        self.execute('natural_object/mineral')


class Disease(TestCoordinator):

    def test_disease_other(self):
        self.execute('disease/disease_other')

    def test_animal_disease(self):
        self.execute('disease/animal_disease')


class Color(TestCoordinator):

    def test_color_other(self):
        self.execute('color/color_other')

    def test_nature_color(self):
        self.execute('color/nature_color')


class Timex(TestCoordinator):

    def test_day_of_week(self):
        self.execute('timex/day_of_week')
