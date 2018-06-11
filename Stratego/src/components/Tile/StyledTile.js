import styled from 'styled-components';
import { calculateTileSize, calculateBorderSize } from '../../computeStyling'

export default styled.div `
    width: ${props => calculateTileSize(props.size)}px;
    height: ${props => calculateTileSize(props.size)}px;
    border-left: ${props => calculateBorderSize(props.size)}px #BBDEFB  solid;
    border-top: ${props => calculateBorderSize(props.size)}px #BBDEFB  solid;
    background: ${props => props.tileColor};
    ${props => props.colNo === props.size -1 && `border-right: ${calculateBorderSize(props.size)}px #BBDEFB solid;`}
    ${props => props.rowNo === props.size -1 && `border-bottom: ${calculateBorderSize(props.size)}px #BBDEFB solid;`}
`