import '../public/styles/global.css'
import Script from 'next/script'
import type { AppProps } from 'next/app'
import { Roboto } from 'next/font/google'
import type { ReactElement, ReactNode } from 'react'
import type { NextPage } from 'next'

export async function getStaticProps() {
  let sslRootCAs = require('ssl-root-cas/latest')
  sslRootCAs.inject()
}

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

function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((page) => page)

  return getLayout(
    <main className={roboto.className}>
      <Component {...pageProps} />
    </main>
  )
}

export default MyApp
