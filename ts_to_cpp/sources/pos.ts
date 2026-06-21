type Int32 = number;
type Position = {
    x: Int32;
    y: Int32;
};type Test = {
    a: string,
    b: string;
    c: Int32;
}

const pos: Position = {x: 1, y: 2};
const pos2:Position = {
    x:8,
    y:(1+pos.x),
};