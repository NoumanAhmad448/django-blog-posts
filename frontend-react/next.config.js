module.exports = {
    webpack(config) {
      config.infrastructureLogging = { debug: /PackFileCache/ }
      return config;
    },
    generateBuildId: async () => {
        return "fjdafjd;fjd;afjd;fja;fdjs;fjsd;laj;l3j24l324j23l4j23l4jl324j23l4j2ldsn;faljdsl;fjl54354075405740574"
    },
  }