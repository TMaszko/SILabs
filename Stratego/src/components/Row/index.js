import React from 'react'
import RowWrapper from './StyledRow'
import Tile from '../Tile'

const Row = ({ size, rowNo, onMove, gameState }) =>
    <RowWrapper size={size}>
        {Array.from({length: size}).map((_,col) => <Tile ownerPlayer={gameState[col]} onMove={onMove} colNo={col} rowNo={rowNo} size={size}/>)}
    </RowWrapper>

export default Row;