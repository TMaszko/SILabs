import React, { Component } from 'react';
import BoardWrapper from './StyledBoard'
import Row from '../Row'

export default class Board extends Component {
    render() {
        return (<BoardWrapper 
        size={this.props.size}>
                {Array.from({length: this.props.size}).map((_, i) => <Row gameState={this.props.gameState[i]} onMove={this.props.onMove} size={this.props.size} rowNo={i}/>)}
        </BoardWrapper>
        )
    }
}