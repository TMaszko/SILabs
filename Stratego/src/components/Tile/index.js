import React from 'react'
import TileWrapper from './StyledTile'

const Tile = ({size, colNo, rowNo, onMove, ownerPlayer}) =>
<TileWrapper
    tileColor={ownerPlayer.color}
    onClick={() => onMove(rowNo, colNo)}
    size={size} 
    colNo={colNo}
    rowNo={rowNo}/>

export default Tile