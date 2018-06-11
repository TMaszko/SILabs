import styled from 'styled-components';
import { calculatePadding, calculateTileSize } from '../../computeStyling';


export default styled.div `
    padding: ${props => calculatePadding(props.size)}px;
    ${props => `height: ${calculateTileSize(props.size) * props.size + 2*calculatePadding(props.size)}px;`}
    ${props => `width: ${calculateTileSize(props.size) * props.size + 2*calculatePadding(props.size)}px;`}
    background: #EFEFEF;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-content: center;
    align-self: center;
    box-shadow: 0px 0px 10px 2px #757575;
    margin: auto 0;
`