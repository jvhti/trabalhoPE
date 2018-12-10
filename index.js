const http = require("http");
const https = require("https");
const fs = require('fs');
const MongoClient = require('mongodb').MongoClient;
const Server = require('mongodb').Server;
const mongoURL = "mongodb://localhost:27017/";
const url = 'http://steamspy.com/api.php?request=all';
var sleep = require('sleep');

const client = new MongoClient(new Server("localhost", 27017));
const connection = client.connect();

let curConnections = 0;

let games = new Array();
let appids = new Array();

let alreadyFinished = new Array();
let failed = new Array();

var contents = fs.readFileSync('success.txt', 'utf8');
contents = contents.split('\n');

for(x of contents){
	const tmp = parseInt(x);
	if(!isNaN(tmp)) 
		alreadyFinished.push(tmp);
}

contents = fs.readFileSync('unsuccess.txt', 'utf8');
contents = contents.split('\n');

for(x of contents){
	const tmp = parseInt(x);
	if(!isNaN(tmp) && !failed.includes(tmp)) 
		failed.push(tmp);
}

appids = failed.filter((x) => { return !alreadyFinished.includes(x); });
failed = Array();

getSteamData();


// http.get(url, function(res){
//     var body = '';

//     res.on('data', function(chunk){
//         body += chunk;
//     });

//     res.on('end', function(){
//         var response = JSON.parse(body);
//         for(const x in response){
//         	const game = response[x];
//         	games.push({_id: game.appid, ...game});
//         }
//         console.log("Got: ", games.length);
// 		putOnDB(true);
//     });
// }).on('error', function(e){
//       console.log("Got an error: ", e);
// });

// async function putOnDB(first){
// 	let news = 0;
// 	let updates = 0;
// 	let sleepTimer = 0;
// 	let wasAppIdsEmpty = !putOnDB;

// 	const connect = await connection;
	
// 	const db = await client.db('pe');
// 	console.log("Starting to update the database...");
// 	while(games.length > 0){
// 		let cur = games.pop();
// 		if(typeof cur === "number") cur = {"_id": cur};
// 		if(alreadyFinished.includes(cur._id)) continue;

// 		const find = await db.collection('games').findOne({"_id": cur._id});
// 		if(appids.length == 0) wasAppIdsEmpty = true;
// 		appids.push(cur._id);

// 		if(!find){
// 			try{
// 				let tmp = await db.collection('games').insertOne(cur);
// 			} catch (e) {
// 				throw e;
// 			}
// 			++news;
// 		}else{
// 			try{
// 				let tmp = await db.collection('games').updateOne({"_id": cur.appid}, {$set: cur});
// 			} catch (e) {
// 				throw e;
// 			}
// 			++updates;
// 		}
// 	}

// 	console.log("Finished getting data from SteamSpy!");
// 	console.log("New: "+news);
// 	console.log("Update: "+updates);

// 	if(wasAppIdsEmpty)
// 		await getSteamData();
// }

// const connect = connection;
// connect.then(() => {
// 	const db = client.db('pe');
// 	db.collection('games').find({}, {_id: 1}).toArray((err, res) => {
// 		if(err) throw err;
// 		appids = res.map((i) => { return i._id; }).filter((x) => { return !alreadyFinished.includes(x) && !failed.includes(x); });
// 		// console.log(appids);
// 		getSteamData();
//    	});

// });


async function getSteamData(){
		console.log("Starting to get data from Steam.");

		while(appids.length > 0){
			console.log("Remaining: "+appids.length);
			const appid = appids.pop();

			if(alreadyFinished.includes(appid)) continue;

			await getMoreData(appid);
			
			++curConnections;

			while(curConnections >= 50){
				sleep.sleep(10);
				curConnections = 0;
			}
		}
}

function getMoreData(appid){
	return new Promise(function(resolve, reject) {  
		console.log("Getting Steam data for app "+appid+"...");
		https.get("https://store.steampowered.com/api/appdetails?appids="+appid, {agent: false}, function(res){
		    var body = '';

		    res.on('data', function(chunk){
		        body += chunk;
		    });

		    res.on('end', function(){
				console.log("\x1b[32m"+"Got data for app "+appid+"!"+"\x1b[0m");
		        var response = JSON.parse(body);
		        const connect = connection;
				connect.then(() => {
					const db = client.db('pe');
					alreadyFinished.push(appid);
					if(!response || response[appid].success == false){
						fs.appendFile("unsuccess.txt", appid+"\n", function(err){
							if(err) throw err;
						});
						console.log("Empty or unsuccessful response");
						resolve();
						return;
					}

					const steamdata = response[appid] && response[appid].data;
					db.collection('games').findOne({"_id": appid}, (err, res) => {
						if(err) throw err;
						if(!res){
							db.collection('games').insertOne({"_id": appid, "appid": appid, steamdata: steamdata})
							console.log("\x1b[32m"+"Added a new not known game "+appid+"!\x1b[0m");
							
						}else db.collection('games').updateOne({"_id": appid}, {$set: {steamdata: steamdata}});

						fs.appendFile("success.txt", appid+"\n", function(err){
							if(err) throw err;
						});
					});

					if((steamdata.dlc || []).length > 0){
						console.log("\x1b[32m"+"Found DLC on "+appid+"! "+steamdata.dlc.length+" DLCs.\x1b[0m");
						appids = appids.concat(steamdata.dlc);
						// putOnDB(false);
					}

					resolve();
				});
		    });
		}).on('error', function(e){
		      console.log("Got an error: ", e);
				fs.appendFile("error.txt", appid+"\n", function(err){
					if(err) throw err;
				});
				reject(e);
			  // process.exit(1);
		});
	});
}