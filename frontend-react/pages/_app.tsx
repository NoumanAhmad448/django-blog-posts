import '../public/styles/global.css'
import Script from 'next/script'
import type { AppProps } from 'next/app'
import { Roboto } from 'next/font/google'
import type { ReactElement, ReactNode } from 'react'
import type { NextPage } from 'next'
import Head from 'next/head'
import { NextRequest, NextResponse } from 'next/server'
import {useState,useEffect} from 'react'
import { Router } from 'next/router'
import Image from 'next/image'


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
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if(process.env.DEBUG){
      console.log(" I have b  een called")
    }
    const start = () => {
      if(process.env.DEBUG){
        console.log("hello world -> start");
      }
      setLoading(true);
    };
    const end = () => {
      if(process.env.DEBUG){
        console.log("finished");
      }
      setTimeout(() => {
        if(process.env.DEBUG){
          console.log('3 sec pause')
        }
      }, 3000);
      setLoading(false);
    };
    Router.events.on("routeChangeStart", start);
    Router.events.on("routeChangeComplete", end);
    Router.events.on("routeChangeError", end);
    return () => {
      Router.events.off("routeChangeStart", start);
      Router.events.off("routeChangeComplete", end);
      Router.events.off("routeChangeError", end);
    };
  }, []);
  return getLayout(
    <>
      {loading ?(
        <section className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-36 bg-white rounded rounded-full">
          <div className="sm:mb-8 sm:flex sm:justify-center">
            <Image src="/images/loader.gif" alt="loader" width={300} height={300}/>
          </div>
        </section>
      )
        :
      <main className={roboto.className}>
        <Component {...pageProps} />
      </main>
    }
    </>
  )
}

export default MyApp
