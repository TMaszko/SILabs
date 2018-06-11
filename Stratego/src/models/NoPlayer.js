import Player from './Player'

export default class NoPlayer extends Player {
    constructor(color) {
        super(-1, color)
    }
}