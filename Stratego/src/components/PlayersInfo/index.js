import React from 'react';
import styled from 'styled-components'
import StyledPlayerInfo from './StyledPlayerInfo';


const PlayersInfoWrapper = styled.div `
    display: flex;
`


const PlayersInfo = ({pointsTable}) =>
    <PlayersInfoWrapper>
        {pointsTable.map((playerPoints ,i) =>
            <StyledPlayerInfo>
            Player {i}: {playerPoints}pt
        </StyledPlayerInfo>)}
    </PlayersInfoWrapper>


export default PlayersInfo