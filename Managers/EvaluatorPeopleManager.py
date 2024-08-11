from Managers.PeopleManager import PeopleManager
from Objects.Person import AlgorithmPerson


class EvaluatorPeopleManager(PeopleManager[AlgorithmPerson]):
    def __init__(self):
        super().__init__()

    def rollback(self):
        pass
