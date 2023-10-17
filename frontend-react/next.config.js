const path = require('path')

module.exports = {
    webpack(config) {
      config.infrastructureLogging = { debug: /PackFileCache/ }
    //   config.resolve.fallback = {
    //     // if you miss it, all the other options in fallback, specified
    //     // by next.js will be dropped.
    //     ...config.resolve.fallback,

    //     fs: false,
    //     path: false // the solution
    //   }
      return config;
    },
    generateBuildId: async () => {
        return "fjdafjd;fjd;afjd;fja;fdjs;fjsd;laj;l3j24l324j23l4j23l4jl324j23l4j2ldsn;faljdsl;fjl54354075405740574"
    },
    // i18n: {
    //     locales: ['en-US', 'zh-Hans'],
    //     defaultLocale: 'en-US',
    //     localeDetection: false,
    // },
    images: {
        // remotePatterns: [
        //   {
        //     protocol: 'https',
        //     hostname: 'nextjs.lyskills.com',
        //     port: '',
        //     pathname: '/my-bucket/**',
        //   },
        // ],
        domains: ["nextjs.lyskills.com","tailwindui.com"],
        minimumCacheTTL: 60,
    },
    sassOptions: {
        includePaths: [path.join(__dirname, 'styles')],
    },
}