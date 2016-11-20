__author__ = 'ASC'

# import js2py


def wildcard(input):

    res = []
    a = []
    for i in input:
        a.append(i[1] + " " + i[0])
    add = js2py.eval_js('function wildcard(input){var output=[],cases=[],wilds=[],patts=[],masks=[];var bits=groupCases(cases);for(var i=0;i<=bits;i++)wilds[i]=[];wildStrings(bits);convertStrings(wilds,patts,"-01","110");convertStrings(wilds,masks,"-01","011");for(var c=0;c<cases.length;c++){for(var i=0,j=Math.pow(2,bits);i<=bits;i++,j /=2){for(var k=0;k<patts[i].length;k++){var patt=patts[i][k];var mask=masks[i][k];var matches=[];for(var d=0;d<cases[c].nums.length;d++){var num=cases[c].nums[d];if(((num^patt)&mask)==mask)matches.push(d);}if(matches.length==j){output.push(wilds[i][k]+" "+cases[c].id);for(var l=j-1;l>=0;l--)cases[c].nums.splice(matches[l],1);}}}}return output;function groupCases(cases){var max=0;for(var i=0;i<input.length;i++){var num=parseInt(input[i],2);if(num>max)max=num;var id=input[i].slice(input[i].indexOf(" ")+1);var pos=0;while(cases[pos]!=undefined&&cases[pos].id!=id)++pos;if(cases[pos]==undefined)cases[pos]={id:id,nums:[]};cases[pos].nums.push(num);}return Math.ceil(Math.log(max)/ Math.log(2));}function wildStrings(len,wild,str){wild=wild||0;str=str||"";for(var i=0;i<3;i++){var w=(i==0)?1:0;var s=str+["-","0","1"][i];if(len>1){wildStrings(len-1,wild+w,s)}else {wilds[bits-wild-w].push(s);}}}function convertStrings(input,output,from,to){for(var i=0;i<input.length;i++){output[i]=[];for(var j=0;j<input[i].length;j++){var str=input[i][j],s="";for(var k=0;k<str.length;k++){s+=to.charAt(from.indexOf(str.charAt(k)));}output[i].push(parseInt(s,2));}}}}')

    for i in add(a):
        if i is None:
            break
        res.append(i.encode("ascii", "ignore"))

    return res