import styled from 'styled-components'
import { calculateTileSize } from '../../computeStyling'

export default styled.div `
    ${props => `height: ${calculateTileSize(props.size)}px;`}
    ${props => `width: ${calculateTileSize(props.size) * props.size}px;`}
    display: flex;
`