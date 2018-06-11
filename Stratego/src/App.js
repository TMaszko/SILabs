import React, {Component} from 'react';
import Board from './components/Board'
import Header from './components/Header'
import styled from 'styled-components'
import Player from './models/Player'
import AIPlayer from './models/AIPlayer'
import PlayersInfo from './components/PlayersInfo';
import GameEngine from './models/GameEngine'
import './App.css';
import NoPlayer from "./models/NoPlayer";


const AppWrapper = styled.div `
  display: flex;
  align-items: center;
  flex-direction: column;
  height: 100%;
  width: 100%;
`

class App extends Component {

    gameEngine = new GameEngine(this.props.size);


    state = {
            diagonals: this.gameEngine.makeAllDiagonals(this.props.size),
            moves: 0,
            end: false,
            pointsTable: [0,0],
            players: [new AIPlayer(0, "green"), new AIPlayer(1, "red")],
            board: Array.from({length: this.props.size}).map(_ => Array.from({length: this.props.size}, _ => {
                return new NoPlayer("#1976D2")
            }))

    };

    componentDidMount() {
        this.state.players[0].getMove(this.move, this.state.board, this.gameEngine, this.state.players, this.state.pointsTable)
    }


    flipPlayers = () => {
        const [playerCurrent, ...otherPlayer] = this.state.players;
        return [...otherPlayer, playerCurrent]
    };

    isPossibleMove = (board, moves) => {
        return moves !== (board.length * board.length);
    };

    updateGameState = (row, col) => {
        const board = [...this.state.board];
        board[row][col] = this.state.players[0]
        return {board, moves: this.state.moves  + 1};
    };

    updatePlayerPoints = (points, currentPlayerNo, pointsTable) => {
        const currentPlayersPoints = pointsTable[currentPlayerNo];
        const newPointsTable = [...pointsTable]
        newPointsTable[currentPlayerNo] = currentPlayersPoints + points;
        return newPointsTable
    }

    isFreeTile = (row, col) => {
        return this.state.board[row][col].no === -1;
    }

    move = (row, col) => {
        if(this.isFreeTile(row, col)) {
            const {board, moves} = this.updateGameState(row, col);
            const points = this.gameEngine.calculatePoints({row, col}, board);
            const isPossibleMove = this.isPossibleMove(board, moves);
            console.log('isPossibleMove: ', isPossibleMove, moves);
            if (!isPossibleMove) {
                console.log('end');
                this.setState({
                    end: true,
                    pointsTable: this.updatePlayerPoints(points, this.state.players[0].no, this.state.pointsTable),
                })
            }
            else {
                this.setState({
                    moves,
                    board,
                    pointsTable: this.updatePlayerPoints(points, this.state.players[0].no, this.state.pointsTable),
                    players: this.flipPlayers()
                }, () => {
                    this.state.players[0].getMove(this.move, this.state.board, this.gameEngine, this.state.players, this.state.pointsTable)
                })
            }
        }
    };

    render() {
        console.log(this.state.pointsTable[0], this.state.pointsTable[1]);
        return (
            <AppWrapper>
                <Header/>
                <PlayersInfo pointsTable={this.state.pointsTable}/>
                {this.state.end && "KONIEC GRY"}
                <Board gameState={this.state.board} onMove={this.move} size={this.props.size}/>
            </AppWrapper>
        )
    }
}

export default App;
