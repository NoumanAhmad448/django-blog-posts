import '../public/styles/global.css'
import '../public/styles/custom.module.scss'
import Script from 'next/script'
import type { AppProps } from 'next/app'
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
})

function MyApp({ Component, pageProps }) {
  const getLayout = Component.getLayout

  return getLayout(
    <main className={roboto.className}>
      <Component {...pageProps} />
    </main>
  )
}

export default MyApp
