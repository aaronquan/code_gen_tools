type Int32 = number;

function check(nums: Int32[]): boolean {
    for(let i = 0; i < nums.length; i++){
        if(isSorted(nums, i)){
            return true;
        }
    }
    return false;
};

function isSorted(nums: Int32[], i: Int32): boolean{
    for(let j = 0; j < nums.length-1; j++){
        const k1 = (j + i) % nums.length;
        const k2 = (j + i + 1) % nums.length;
        if(nums[k1] > nums[k2]){
            return false;
        }
    }
    return true;
}