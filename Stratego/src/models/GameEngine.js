import Player from "./Player";

export default class GameEngine {
    constructor(size) {
        this.size = size;
        this.diagonals = this.makeAllDiagonals(size);
        this.board = Array.from({length: size}).map(_ => Array.from({length: size}, _ => {
            return new Player(-1, "#1976D2")
        }))
    }

    makeAllDiagonals = (size) => {
        const makeDiagonals = (size, shiftColFn, shiftRowFn, startRow, startCol, traverseRowFn, traverseColFn) => {
            let result = []
            let shift = 0;
            let _startCol = startCol;
            let _startRow = startRow;
            while (shift < size - 1) {
                let j = shiftColFn(shift, _startCol);
                let i = _startRow;
                shift++;
                let membersOfDiagonal = []
                while (j > -1 && j < size) {
                    membersOfDiagonal.push({row: i, col: j});
                    i = traverseRowFn(i)
                    j = traverseColFn(j);
                }
                result.push(membersOfDiagonal);
            }
            shift = 1;
            _startCol = 0;
            while (shift < size - 1) {
                let j = _startCol
                let i = shiftRowFn(shift, _startRow);
                shift++;
                let membersOfDiagonal = []
                while (i > -1 && i < size) {
                    membersOfDiagonal.push({row: i, col: j});
                    i = traverseRowFn(i)
                    j = traverseColFn(j);
                }
                result.push(membersOfDiagonal);
            }
            return result;
        }

        const allDiagonalsInOneDirection = makeDiagonals(size, (shift, colNo) => colNo - shift, (shift, rowNo) => rowNo + shift, 0, size - 2, (rowNo) => rowNo + 1, colNo => colNo + 1);
        const allDiagonalsInInverseDirection = makeDiagonals(size, (shift, colNo) => colNo - shift, (shift, rowNo) => rowNo - shift, size - 1, size - 2, (rowNo) => rowNo - 1, colNo => colNo + 1);
        const allDiagonals = allDiagonalsInOneDirection.concat(allDiagonalsInInverseDirection);
        return allDiagonals;
    }
    calculatePoints = (coords, board) => {
        return this.calculatePointsFromClosures(coords, board)
    };

    calculatePointsFromClosures = (coords, board) => {
        const pointsFromRow = this.checkClosureInRow(coords.row, board) && board.length;
        const pointsFromColumn = this.checkClosureInColumn(coords.col, board) && board.length;
        const pointsFromDiagonals = this.checkClosureDiagonals(coords, board);
        console.log('rowPoints: '+ pointsFromRow, 'colPoints: ' + pointsFromColumn, 'diagonalsPoints: ' + pointsFromDiagonals);
        return pointsFromRow + pointsFromColumn + pointsFromDiagonals;
    };

    flipPlayers = (players) => {
        const [playerCurrent, ...otherPlayer] = players;
        return [...otherPlayer, playerCurrent]
    };
    checkClosureInRow = (rowNo, board) => {
        return board[rowNo].every(el => el.no !== -1)
    }

    checkClosureInColumn = (colNo, board) => {
        return board.every(row => row[colNo].no !== -1)
    }

    updatePlayerPoints = (points, currentPlayerNo, pointsTable) => {
        const currentPlayersPoints = pointsTable[currentPlayerNo];
        const newPointsTable = [...pointsTable]
        newPointsTable[currentPlayerNo] = currentPlayersPoints + points;
        return newPointsTable
    }

    checkClosureDiagonals = (coords, board) => {
        const {row, col} = coords;
        const matchingDiagonalsWithCoords =  this.diagonals.filter(diagonal => diagonal.findIndex(el => el.row === row && el.col === col) !== -1)
        return matchingDiagonalsWithCoords.reduce((acc, diagonal) => acc + (diagonal.every(el => board[el.row][el.col].no !== -1) && diagonal.length),0);
    }
}

