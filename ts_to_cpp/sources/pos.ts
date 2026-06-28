type  Int32 = number;
type Position = {
    x: Int32;
    y: Int32;
};type Test = {
    a?: string,
    b: string;
    c: Int32 | undefined;
}

const vd = () => {};

type NT<T extends Int32, V> = T | null

function a(){
    return 1;
}

function gen<T>(a: T): T{
    return a;
}

const v = 10;
const d = (1 + 5);

const   pos: Position = {x: 1, y: 2};
const pos2:Position = {
    x:8,
    y:(v+pos.x),
};