module.exports = {
  publicPath: '/sudoku',
  outputDir: '../server/templates',
  // assetsのディレクトリ構造がVueとDjangoで違うため、環境によって書き換える
  assetsDir: process.env.NODE_ENV === 'production' ? '../static' : '',
  devServer: {
    proxy: 'http://localhost:8000'
  },
  css: {
    loaderOptions: {
      sass: {
        data: '@import "./src/assets/scss/colors.scss";'
      }
    }
  }


}