
export const calculatePadding = size => size * 2;

export const calculateTileSize = size => (window.innerHeight - 2*calculatePadding(size)-40)/(size *2)

export const calculateBorderSize = size => calculateTileSize(size)/15