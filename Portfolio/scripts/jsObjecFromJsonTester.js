var path = require('path'); //系统路径模块
var fs = require('fs'); //文件模块

var file = path.join(__dirname,'echarts.json'); //文件路径，__dirname为当前运行js文件的目录

function getPortfolioData()
{
    console.log(file)
    //读取json文件
    fs.readFile(file, 'utf-8', function(err, data) {
        if (err) {
            console.log(err)
            console.log('文件读取失败');
        } else {
            var obj = JSON.parse(data)
            console.log(obj)
            return obj
        }
    });
}
//var data = getPortfolioData()
//jsonStr = JSON.stringify(data)
//console.log(JSON.stringify(data))

//var filePath = path.join(__dirname, 'config/echarts.json'); //文件路径，__dirname为当前运行js文件的目录

//fs.writeFile(filePath, jsonStr, 'utf-8', function(err) {
//    if (err) {
//        throw err;
//    }
//});
