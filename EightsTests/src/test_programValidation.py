
import io
import sys
import pytest
from PuzzleSolver import *
from manhattan import manhattan_search , timeout_handler
from astar import astar
from price import price, weighted_mdistance

"""PuzzleSolver.py tests"""

"""Test to verify that the is_solvable function accurately determines if 
 a given puzzle state is solvable or not"""
def test_is_solvable():
    solvable_state = [
        [1, 2, 3],
        [5, 6, 0],
        [7, 8, 4]
    ]
    unsolvable_state = [
        [1, 2, 3],
        [5, 6, 8],
        [7, 0, 4]
    ]
    assert is_solvable(solvable_state, 3) == True
    assert is_solvable(unsolvable_state, 3) == False

"""Test to ensure that the manhattan_distance function correctly calculates 
 the Manhattan distance for a given puzzle state"""
def test_manhattan_distance():
    state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    assert manhattan_distance(state) == 1 


""" Test to verify the goal state itself is recognized as complete"""
def test_is_complete_with_goal_state():
    goal_state = generate_goal_state(3, 3)
    assert is_complete(goal_state, goal_state) == True



""" Test to ensure that generate_child_nodes correctly identifies the valid moves
 for a given state"""
def test_generate_child_nodes():
    state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    empty_i, empty_j, possible_moves = generate_child_nodes(state)
    assert (empty_i, empty_j) == (1, 1)
    assert set(possible_moves) == {(0, 1), (1, 0), (1, 2), (2, 1)}



""" Test to ensure that the goal state is correctly generated for a given dimension"""
def test_generate_goal_state():
    expected_3x3 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    assert generate_goal_state(3, 3) == expected_3x3



"""The following are very basic input validation specific tests that probably require more testing to be thorough,
 but due to time constraints i mainly tested 3x3 grid inputs"""


def test_validate_dimensions_valid():
    """Test that valid grid dimensions are correctly identified."""
    validate_dimensions(3, 3)
    validate_dimensions(2, 2)
    validate_dimensions(9, 9)

def test_validate_dimensions_invalid():
    """Test that invalid grid dimensions raise an error."""
    with pytest.raises(ValueError):
        validate_dimensions(101, 3)  
    with pytest.raises(ValueError):
        validate_dimensions(3, 101)  

def test_validate_values_valid():
    """Test that a correct set of grid values doesn't raise an error."""
    validate_values(list(range(9)), 3, 3)
    validate_values(list(range(4)), 2, 2)
    validate_values(list(range(121)), 11, 11)

def test_validate_values_mismatch():
    """Test that a mismatch in the number of grid values raises an error."""
    with pytest.raises(ValueError):
        validate_values(list(range(8)), 3, 3)
    with pytest.raises(ValueError):
        validate_values(list(range(10)), 3, 3)

def test_validate_values_invalid():
    """Test that invalid grid values raise an error."""
    with pytest.raises(ValueError):
        validate_values(list(range(10)), 3, 3)
    with pytest.raises(ValueError):
        validate_values(list(range(5)), 2, 2)
    with pytest.raises(ValueError):
        validate_values(list(range(1, 122)), 11, 11)






"""The following are Manhattan specific tests"""

""" Test to ensure that the solution produced by manhattan_search correctly 
transforms a given initial state to the goal state when the moves are applied"""    

def test_apply_moves_manhattan():
    initial_state = random_solvable_state(3, 3)
    _, moves = manhattan_search(initial_state, 3, 3)
    result_state = apply_moves_to_state(initial_state, moves)
    expected_result = generate_goal_state(3, 3)
    assert result_state == expected_result

"""This test ensures that when the `manhattan_search` prints "timeout exception" and returns (-1, []) when it encounters a sufficiently large/ complex state that it can't solve in a minute.
Because of technical difficulties with the Timeout Error class and the signal library, I couldn't test the timeout exception directly. Instead, I test the printed output instead of the exception to ensure that we are actually timing out.
    """
def test_timeout_manhattan():
    initial_state = random_solvable_state(10, 10)
    
    # Replace the standard output with our own stream
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    
    result = manhattan_search(initial_state, 10, 10)
    
    # Reset standard output to its original value
    sys.stdout = sys.__stdout__
    
    # Assert the printed output and the return value
    assert "timeout exception" in capturedOutput.getvalue()
    assert result == (-1, [])

# Test to ensure that the manhattan_search identifies an already solved state 
# and returns a status of 1 with no moves
def test_already_solved_state_manhattan():
    solved_state = generate_goal_state(3, 3)
    status, moves = manhattan_search(solved_state, 3, 3)
    assert status == 1
    assert len(moves) == 0

# Test to ensure that unsolvable states will cause manhattan_search to either time out or empty its priority queue
# by returning a status of -1
def test_unsolvable_state_manhattan():
    unsolvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    status, _ = manhattan_search(unsolvable_state, 3, 3)
    assert status == -1

"""The following are A* specific tests"""


""" Test to ensure that the solution produced by astar correctly 
transforms a given initial state to the goal state when the moves are applied"""    

def test_apply_moves_astar():
    initial_state = random_solvable_state(3, 3)
    _, moves = astar(initial_state, 3, 3)
    result_state = apply_moves_to_state(initial_state, moves)
    expected_result = generate_goal_state(3, 3)
    assert result_state == expected_result

#Same concept as manhattanSearch
def test_timeout_astar():
    initial_state = random_solvable_state(10, 10)
    
    # Replace the standard output with our own stream
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    
    result = astar(initial_state, 10, 10)
    
    # Reset standard output to its original value
    sys.stdout = sys.__stdout__
    
    # Assert the printed output and the return value
    assert "timeout exception" in capturedOutput.getvalue()
    assert result == (-1, [])

# Test to ensure that the astar identifies an already solved state 
# and returns a status of 1 with no moves
def test_already_solved_state_astar():
    solved_state = generate_goal_state(3, 3)
    status, moves = astar(solved_state, 3, 3)
    assert status == 1
    assert len(moves) == 0

# Test to ensure that unsolvable states will cause astar to either time out or empty its priority queue
# by returning a status of -1
def test_unsolvable_state_astar():
    unsolvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    status, _ = astar(unsolvable_state, 3, 3)
    assert status == -1


"""The following are Price specific tests"""

""" Test to ensure that the solution produced by price correctly 
transforms a given initial state to the goal state when the moves are applied"""    

def test_apply_moves_price():
    initial_state = random_solvable_state(3, 3)
    _, moves,placeholder = price(initial_state, 3, 3)
    result_state = apply_moves_to_state(initial_state, moves)
    expected_result = generate_goal_state(3, 3)
    assert result_state == expected_result



def test_timeout_price():
    initial_state = random_solvable_state(10, 10)
    
    # Replace the standard output with our own stream
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    
    result = price(initial_state, 10, 10)
    
    # Reset standard output to its original value
    sys.stdout = sys.__stdout__
    
    # Assert the printed output and the return value
    assert "timeout exception" in capturedOutput.getvalue()
    assert result == (-1, [])

# Test to ensure that the manhattan_search identifies an already solved state 
# and returns a status of 1 with no moves
def test_already_solved_state_price():
    solved_state = generate_goal_state(3, 3)
    status, moves,_ = price(solved_state, 3, 3)
    assert status == 1
    assert len(moves) == 0

# Test to ensure that unsolvable states will cause manhattan_search to either time out or empty its priority queue
# by returning a status of -1
def test_unsolvable_state_price():
    unsolvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    status, _ = price(unsolvable_state, 3, 3)
    assert status == -1


"""Test to ensure that the manhattan_distance function correctly calculates 
 the Manhattan distance for a given puzzle state"""
def test_weighted_manhattan_distance():
    state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    assert weighted_mdistance(state) == 8 