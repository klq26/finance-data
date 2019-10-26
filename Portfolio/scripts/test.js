var path = require('path'); //系统路径模块
var fs = require('fs'); //文件模块

var file = path.join(__dirname, 'pySample.json'); //文件路径，__dirname为当前运行js文件的目录

//读取json文件
fs.readFile(file, 'utf-8', function(err, data) {
	if (err) {
		console.log('文件读取失败');
	} else {
		var obj = JSON.parse(data)
		console.log(obj)
	}
});

//getPortfolioData().toJSONString();