const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  mode: "development",
  // entry: {
  //   index: "./src/js/index.js",
  //   print: "./src/js/print.js",
  // },
  entry: "./src/js/index.js",
  devtool: "inline-source-map",
  // devServer: {
  //   static: {
  //     directory: path.join(__dirname, "dist"),
  //   },
  //   compress: true,
  //   liveReload: true,
  //   watchFiles: ["dist/*", "dist/**/*"],
  //   port: 9000,
  //   proxy: {
  //     "/proxy": "https://127.0.0.1:9000",
  //   },
  // },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "index.html"),
      minify: false,
    }),
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
  ],
  output: {
    filename: "js/[name].bundle.js",
    path: path.resolve(__dirname, "dist"),
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
  optimization: {
    // runtimeChunk: "single",
    splitChunks: {
      chunks: "all",
      maxInitialRequests: Infinity,
      minSize: 0,
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name(module) {
            const packageName = module.context.match(
              /[\\/]node_modules[\\/](.*?)([\\/]|$)/
            )[1];

            return `${packageName.replace("@", "")}`;
          },
        },
      },
    },
    minimize: true,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
};
