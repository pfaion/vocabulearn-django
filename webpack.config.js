var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	context: __dirname,
	entry: [
		'webpack-dev-server/client?http://localhost:3000',
		'webpack/hot/only-dev-server',
		'./assets/js/index'
	],
	output: {
		path: path.resolve('./assets/bundles/'),
		filename: 'app.js',
		publicPath: 'http://localhost:3000/assets/bundles/'
	},

	plugins: [
		new webpack.HotModuleReplacementPlugin(),
		//new webpack.NoErrorsPlugin(), // don't reload if there is an error
		new BundleTracker({filename: './webpack-stats.json'}),
	],
	
	performance: {
		hints: false
	},

	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				loader: 'babel-loader',
			},
			{
				test: /\.vue$/,
				loader: 'vue-loader',
				options: {
					loaders: {
						scss: 'style-loader!css-loader!sass-loader'
					}
				}
			},
			{
				test: /\.s[a|c]ss$/,
				loader: 'style!css!sass'
			}
		],
	},
	
	resolve: {
		alias: {vue: 'vue/dist/vue.js'}
	},
	mode: 'production'

};