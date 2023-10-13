import { useRouter } from 'next/router'

const Home = ({ Component, pageProps }) => {
  const router = useRouter()
  return (
    <section>
      <div> Given post id {router.query.id} </div>
    </section>
  )
}


export default Home
