import '../public/styles/global.css'
import Script from 'next/script'
import type { AppProps } from 'next/app'
import { Roboto } from 'next/font/google'
import type { ReactElement, ReactNode } from 'react'
import type { NextPage } from 'next'
import Head from 'next/head'
import { NextRequest, NextResponse } from 'next/server'


const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
})

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode
}

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout
}

export const getS = async ({ req }) => {
  const logger = require("pino")()
  // import { headers } from 'next/headers'

  const csp = {}
  logger.info("content security policy")
  logger.info(`content-security-policy ${req.headers}`)

  // res.getHeaders()['content-security-policy']?.split(';').filter(Boolean).forEach(part => {
  //   const [directive, ...source] = part.split(' ');
  //   csp[directive] = source.map(s => s.slice(1, s.length - 1));
  // })
  if(process.env.DEBUG){
    logger.info("here is nonce")
    logger.info(csp['default-src'])
  }
  return {
    // nonce: csp['default-src']?.find(s => s.startsWith('nonce-')).split('-')[1],
    nonce: ''
  }
}


function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((page) => page)

  return getLayout(
    <>
      <main className={roboto.className}>
        <Component {...pageProps} />
      </main>
    </>
  )
}

export default MyApp
