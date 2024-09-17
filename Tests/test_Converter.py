import pytest
import Managers.Converter as Converter
from Managers.EvaluatorPeopleManager import EvaluatorPeopleManager
from Managers.SystemPeopleManager import SystemPeopleManager
from Managers.PeopleManager import PeopleContainer
from Objects.Person import AlgorithmPerson, Person


def assert_person_conversion(person, algorithm_person, where):
    assert algorithm_person.start_pos == person.start_pos
    assert algorithm_person.destination == person.destination
    assert algorithm_person.current_affiliation == where
    assert algorithm_person.original_affiliation == where


def test_convert_person():
    person = Person(0, 1)
    algorithm_person = Converter._convert_person(person, None)
    assert isinstance(algorithm_person, AlgorithmPerson)
    assert_person_conversion(person, algorithm_person, None)

    person = Person(0, 1)
    algorithm_person = Converter._convert_person(person, 0)
    assert isinstance(algorithm_person, AlgorithmPerson)
    assert_person_conversion(person, algorithm_person, 0)
