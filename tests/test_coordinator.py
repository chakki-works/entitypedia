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
        self.execute('name/name_other')

    def test_person(self):
        self.execute('name/person')

    def test_god(self):
        self.execute('name/god')

    def test_character(self):
        self.execute('name/character')


class Organization(TestCoordinator):

    def test_organizaton_other(self):
        self.execute('organization/organization_other')

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

    def test_company_group(self):
        self.execute('organization/corporation/company_group')

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

    def test_location_other(self):
        self.execute('location/location_other')

    def test_spa(self):
        self.execute('location/spa')

    def test_gpe_other(self):
        self.execute('location/gpe/gpe_other')

    def test_city(self):
        self.execute('location/gpe/city')

    def test_county(self):
        self.execute('location/gpe/county')

    def test_province(self):
        self.execute('location/gpe/province')

    def test_country(self):
        self.execute('location/gpe/country')

    def test_region_other(self):
        self.execute('location/region/region_other')

    def test_continental_region(self):
        self.execute('location/region/continental_region')

    def test_domestic_region(self):
        self.execute('location/region/domestic_region')

    def test_geological_region_other(self):
        self.execute('location/geological_region/geological_region_other')

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

    def test_address_other(self):
        self.execute('location/address/address_other')


class Facility(TestCoordinator):

    def test_facility_other(self):
        self.execute('facility/facility_other')

    def test_archaeological_place_other(self):
        self.execute('facility/archaeological_place/archaeological_place_other')

    def test_tumulus(self):
        self.execute('facility/archaeological_place/tumulus')

    def test_goe_other(self):
        self.execute('facility/goe/goe_other')

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

    def test_line_other(self):
        self.execute('facility/line/line_other')

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

    def test_clothing(self):
        self.execute('product/clothing')

    def test_money_form(self):
        self.execute('product/money_form')

    def test_drug(self):
        self.execute('product/drug')

    def test_weapon(self):
        self.execute('product/weapon')

    def test_award(self):
        self.execute('product/award')

    def test_decoration(self):
        self.execute('product/decoration')

    def test_offense(self):
        self.execute('product/offense')

    def test_class(self):
        self.execute('product/class')

    def test_vehicle_other(self):
        self.execute('product/vehicle/vehicle_other')

    def test_car(self):
        self.execute('product/vehicle/car')

    def test_train(self):
        self.execute('product/vehicle/train')

    def test_aircraft(self):
        self.execute('product/vehicle/aircraft')

    def test_spaceship(self):
        self.execute('product/vehicle/spaceship')

    def test_ship(self):
        self.execute('product/vehicle/ship')

    def test_food_other(self):
        self.execute('product/food/food_other')

    def test_dish(self):
        self.execute('product/food/dish')

    def test_art_other(self):
        self.execute('product/art/art_other')

    def test_picture(self):
        self.execute('product/art/picture')

    def test_broadcast_program(self):
        self.execute('product/art/broadcast_program')

    def test_movie(self):
        self.execute('product/art/movie')

    def test_music(self):
        self.execute('product/art/music')

    def test_book(self):
        self.execute('product/art/book')

    def test_newspaper(self):
        self.execute('product/printing/newspaper')

    def test_magazine(self):
        self.execute('product/printing/magazine')

    def test_culture(self):
        self.execute('product/doctrine_method/culture')

    def test_academic(self):
        self.execute('product/doctrine_method/academic')

    def test_religion(self):
        self.execute('product/doctrine_method/religion')

    def test_sport(self):
        self.execute('product/doctrine_method/sport')

    def test_style(self):
        self.execute('product/doctrine_method/style')

    def test_theory(self):
        self.execute('product/doctrine_method/theory')

    def test_movement(self):
        self.execute('product/doctrine_method/movement')

    def test_plan(self):
        self.execute('product/doctrine_method/plan')

    def test_rule_other(self):
        self.execute('product/rule/rule_other')

    def test_treaty(self):
        self.execute('product/rule/treaty')

    def test_law(self):
        self.execute('product/rule/law')

    def test_language_other(self):
        self.execute('product/language/language_other')

    def test_national_language(self):
        self.execute('product/language/national_language')

    def test_title_other(self):
        self.execute('product/title/title_other')

    def test_position_vocation(self):
        self.execute('product/title/position_vocation')

    def test_unit_other(self):
        self.execute('product/unit/unit_other')

    def test_currency(self):
        self.execute('product/unit/currency')


class Event(TestCoordinator):

    def test_event_other(self):
        self.execute('event/event_other')

    def test_occasion_other(self):
        self.execute('event/occasion/occasion_other')

    def test_religious_festival(self):
        self.execute('event/occasion/religious_festival')

    def test_game(self):
        self.execute('event/occasion/game')

    def test_conference(self):
        self.execute('event/occasion/conference')

    def test_incident_other(self):
        self.execute('event/incident/incident_other')

    def test_war(self):
        self.execute('event/incident/war')

    def test_natural_phenomenon_other(self):
        self.execute('event/natural_phenomenon/natural_phenomenon_other')

    def test_natural_disaster(self):
        self.execute('event/natural_phenomenon/natural_disaster')

    def test_earthquake(self):
        self.execute('event/natural_phenomenon/earthquake')


class NaturalObject(TestCoordinator):

    def test_natural_object_other(self):
        self.execute('natural_object/natural_object_other')

    def test_element(self):
        self.execute('natural_object/element')

    def test_compound(self):
        self.execute('natural_object/compound')

    def test_mineral(self):
        self.execute('natural_object/mineral')

    def test_living_thing_other(self):
        self.execute('natural_object/living_thing/living_thing_other')

    def test_fungus(self):
        self.execute('natural_object/living_thing/fungus')

    def test_mollusc_arthropod(self):
        self.execute('natural_object/living_thing/mollusc_arthropod')

    def test_insect(self):
        self.execute('natural_object/living_thing/insect')

    def test_fish(self):
        self.execute('natural_object/living_thing/fish')

    def test_amphibia(self):
        self.execute('natural_object/living_thing/amphibia')

    def test_reptile(self):
        self.execute('natural_object/living_thing/reptile')

    def test_bird(self):
        self.execute('natural_object/living_thing/bird')

    def test_mammal(self):
        self.execute('natural_object/living_thing/mammal')

    def test_flora(self):
        self.execute('natural_object/living_thing/flora')


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

    def test_date(self):
        self.execute('timex/date')

    def test_era(self):
        self.execute('timex/era')


class Concept(TestCoordinator):

    def test_concept(self):
        self.execute('concept')
