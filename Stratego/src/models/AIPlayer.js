import Player from './Player'
import NoPlayer from "./NoPlayer";

const deepCopy = (board) => {
    return board.map(row => row.map(cell => {
        if (cell.no === -1) {
            return new NoPlayer(cell.color);
        } else if (cell instanceof AIPlayer) {
            return new AIPlayer(cell.no, cell.color)
        } else {
            return new Player(cell.no, cell.color);
        }
    }))
}


const generateAllPossibleMovesOneStepAhead = (player, board) => {
    return board.reduce((acc, row, rowNo) => {
        return acc.concat(row.reduce((accInRow, cell, colNo) => {
            let _possibleState = [];
            if (cell.no === -1) {
                _possibleState = deepCopy(board);
                _possibleState[rowNo][colNo] = player;
                let move = {row: rowNo, col: colNo};
                _possibleState = {move, possibleBoard: _possibleState}
            }
            return accInRow.concat(_possibleState);
        }, []))
    }, [])
}


const generateNextPossibleMove = (player, board, i, j) => {
    console.log('board lol', board, i , j);
    let _startCol = j % board.length;
    let _startRow = i + ~~(j / board.length)
    console.log('startCol: ', _startCol, 'startRow', _startRow);
    while (_startRow < board.length) {
        while (_startCol < board.length) {
            const cell = board[_startRow][_startCol];
            if (cell.no === -1) {
                let _possibleBoard = deepCopy(board);
                _possibleBoard[_startRow][_startCol] = player;
                console.log('lul', _possibleBoard)
                console.log('lul')
                return {move: {row: _startRow, col: _startCol}, _possibleBoard};
            }
            _startCol++;
        }
        _startCol = 0;
        _startRow++;
    }
    console.log('nic');
    return {_possibleBoard: []};
}


const randomlyNextPossibleMove = (player, board, movesAlreadyTaken) => {
    console.log(movesAlreadyTaken);
    let possibleCells = board.map((row,i) => row.map((col, j) =>({row: i, col: j}))).reduce((acc, curr) => acc.concat(curr), [])
        console.log(possibleCells);
    possibleCells = possibleCells.filter(({row, col}) => !movesAlreadyTaken.some(el => row === el.row && el.col === col) && board[row][col].no === -1 )
    console.log('after filter', possibleCells)
    const randomCell = possibleCells[~~(Math.random() * possibleCells.length)];
    if(possibleCells.length === 0) {
        return {_possibleBoard: []}
    } else {
        const _possibleBoard = deepCopy(board);
        _possibleBoard[randomCell.row][randomCell.col] = player;
        return {move: {...randomCell}, _possibleBoard};
    }
}


const heuristicSumOfDifference = (points, currentPossiblePoints, type) => {
    if (type === "MAX") {
        return points + currentPossiblePoints;
    } else {
        return points - currentPossiblePoints;
    }
}
const heuristicOnlySumOfMaxPoints =  (points, currentPossiblePoints, type) => {
    if (type === "MAX") {
        return points + currentPossiblePoints;
    } else {
        return points;
    }
}

const heuristicOnlySumOfMinPoints = (points, currentPossiblePoints, type) => {
    if (type === "MAX") {
        return points;
    } else {
        return points - currentPossiblePoints;
    }
}


const minmax = (players, pointsTable, board, heuristic, depth, gameEngine, points, type) => {
    if (depth > 0) {
        const nextLevel = generateAllPossibleMovesOneStepAhead(players[0], board);
        console.log(nextLevel.reduce((acc, curr) =>
                acc.concat([curr.possibleBoard])
            , []))
        let max = {move: {}, points: -Infinity};
        let min = {move: {}, points: Infinity};
        if (nextLevel.length !== 0) {
            nextLevel.forEach(({move, possibleBoard}) => {
                const currentPossiblePoints = gameEngine.calculatePoints(move, possibleBoard);
                const updatedPointsTable = gameEngine.updatePlayerPoints(currentPossiblePoints, players[0].no, pointsTable)
                const result = minmax(gameEngine.flipPlayers(players), updatedPointsTable, possibleBoard, heuristic, depth - 1, gameEngine, heuristic(points, currentPossiblePoints, type), type === "MAX" ? "MIN" : "MAX");
                if (type === "MAX") {
                    if (max.points < result.points) {
                        max = {move, points: result.points}
                        console.log('max: ', max, ' move: ', move);
                    }
                } else {
                    if (result.points < min.points) {
                        min = {move, points: result.points}
                        console.log('min: ', min, ' move: ', move);
                    }
                }
            });
            return type === "MAX"? {...max} : {...min}
        } else {
            return {points};
        }

    } else {
        console.log(points);
        return {points};
    }
}

const alfabeta = (players, pointsTable, board, heuristic, depth, gameEngine, points, type, alfa, beta, movesDone) => {
    if (depth > 0) {
        console.log('depth ', depth);
        let lastMove = {}
        let startSearchCord = {row: 0, col: 0};
        let _alfa = {
            ...alfa
        }
        let _beta = {
            ...beta
        }
        let max = {move: {}, points: -Infinity};
        let min = {move: {}, points: Infinity};
        while (_beta.points > _alfa.points) {
            console.log('depth', depth)
            // const {move, _possibleBoard} = generateNextPossibleMove(players[0], board, startSearchCord.row, startSearchCord.col);
            const {move, _possibleBoard} = randomlyNextPossibleMove(players[0], board, movesDone);
            console.log('possibleBoard', _possibleBoard)
            console.log('possibleMove', move);
            console.log('TYPE', type)
            console.log('alfa', _alfa, 'beta', _beta);
            let result = {points}
            if (_possibleBoard.length !== 0) {
                movesDone = movesDone.concat(move);
                console.log(movesDone)
                startSearchCord = {
                    col: move.col + 1,
                    row: move.row
                }

                const currentPossiblePoints = gameEngine.calculatePoints(move, _possibleBoard);
                console.log('powinien wejsc do rekurencji!: ');
                result = alfabeta(gameEngine.flipPlayers(players), pointsTable, _possibleBoard, heuristic, depth - 1, gameEngine, heuristic(points, currentPossiblePoints, type), type === "MAX" ? "MIN" : "MAX", _alfa, _beta, []);
                if (type === "MAX") {
                    if (_alfa.points < result.points) {
                        _alfa = {move, points: result.points}
                    }
                    if (max.points < result.points) {
                        max = {move, points: result.points}
                        console.log('max: ', max, ' move: ', move);
                    }
                } else {
                    if (result.points < _beta.points) {
                        _beta = {move, points: result.points}
                        console.log('beta: ', _beta, ' move: ', move);
                    }
                    if (result.points < min.points) {
                        min = {move, points: result.points}
                        console.log('min: ', min, ' move: ', move);
                    }
                }

            } else {
                return type === "MAX"? {..._alfa, points: _alfa.points === -Infinity ? points : _alfa.points} :
                    {..._beta, points: _beta.points === -Infinity ? points : _beta.points}
                }
        }
        return type === "MAX"? {..._alfa} : {..._beta}
    } else {
        debugger;
        // console.log()
        // console.log(points)
        return {points};
    }
}


export default class AIPlayer extends Player {
    constructor(no, color) {
        super(no, color);
    }

    getMove = (mover, board, gameEngine, players, pointsTable) => {
        setTimeout(() => {
            // const alg = minmax(players, pointsTable, board, (points, currentPossiblePoints, type) => {
            //     if (type === "MAX") {
            //         return points + currentPossiblePoints;
            //     } else {
            //         return points - currentPossiblePoints;
            //     }
            // }, 2, gameEngine, 0, "MAX")
            let algDecision =players[0].no === 0? minmax(players, pointsTable, board, (points, currentPossiblePoints, type) => {
                    if (type === "MAX") {
                        return points + currentPossiblePoints;
                    } else {
                        return points - currentPossiblePoints;
                    }
                }, 3, gameEngine, 0, "MAX") : alfabeta(players, pointsTable, board, (points, currentPossiblePoints, type) => {
                if (type === "MAX") {
                    return points + currentPossiblePoints;
                } else {
                    return points - currentPossiblePoints;
                }
            }, 5 ,gameEngine, 0,"MAX", {points: -Infinity}, {points: Infinity},[])
            console.log(algDecision)

            mover(algDecision.move.row, algDecision.move.col);
        }, 200)
    }
}