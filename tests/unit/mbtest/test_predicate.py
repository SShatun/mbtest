# encoding=utf-8
import logging

import pytest
from hamcrest import assert_that, instance_of

from mbtest.imposters import Predicate
from mbtest.imposters.predicates import AndPredicate, BasePredicate, OrPredicate, TcpPredicate
from tests.utils.builders import PredicateBuilder

logger = logging.getLogger(__name__)


def test_structure_path():
    expected_predicate = Predicate(path="/darwin")
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert_that(predicate, instance_of(Predicate))
    assert predicate.path == expected_predicate.path


def test_structure_body():
    expected_predicate = Predicate(body="darwin")
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.body == expected_predicate.body


def test_structure_method():
    expected_predicate = Predicate(method="GET")
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.method == expected_predicate.method


def test_structure_query():
    expected_predicate = Predicate(query={"key": "value"})
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.query == expected_predicate.query


def test_structure_headers():
    expected_predicate = Predicate(headers={"key": "value"})
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.headers == expected_predicate.headers


def test_structure_operator():
    expected_predicate = Predicate(operator="deepEquals")
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.operator == expected_predicate.operator


def test_structure_xpath():
    expected_predicate = Predicate(xpath="darwin")
    predicate_structure = expected_predicate.as_structure()
    predicate = BasePredicate.from_structure(predicate_structure)
    assert predicate.xpath == expected_predicate.xpath


def test_invalid_operator():
    expected_predicate = Predicate(operator="deepEquals")
    predicate_structure = expected_predicate.as_structure()
    # Adds another operator
    predicate_structure["equals"] = {}
    with pytest.raises(Predicate.InvalidPredicateOperator):
        Predicate.from_structure(predicate_structure)


def test_and_predicate():
    expected_predicate = AndPredicate(
        PredicateBuilder(path="left").build(), PredicateBuilder(path="right").build()
    )
    structure = expected_predicate.as_structure()

    # When
    actual = BasePredicate.from_structure(structure)

    # Then
    assert_that(actual, instance_of(AndPredicate))
    assert actual.left.path == "left"
    assert actual.right.path == "right"


def test_or_predicate():
    expected_predicate = OrPredicate(
        PredicateBuilder(path="left").build(), PredicateBuilder(path="right").build()
    )
    structure = expected_predicate.as_structure()

    # When
    actual = BasePredicate.from_structure(structure)

    # Then
    assert_that(actual, instance_of(OrPredicate))
    assert actual.left.path == "left"
    assert actual.right.path == "right"


def test_tcp_predicate():
    # Given
    expected_predicate = TcpPredicate(data="somedata")
    structure = expected_predicate.as_structure()

    # When
    actual = BasePredicate.from_structure(structure)

    # Then
    assert_that(actual, instance_of(TcpPredicate))
    assert actual.data == "somedata"
