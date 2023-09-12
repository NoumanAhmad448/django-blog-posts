import Head from 'next/head'
export default async function Home() {
  try{
    const data = await fetch("localhost:8000/api/posts", {
      method: "POST"
    })
    const response = await data.json()
    console.log(response)
  }
  catch(error){
    console.error(error.message)
  }

  return (
    <div>
      <Head>
        <title>  </title>
        <meta name="favico.ico" content='./favico.ico'/>
      </Head>
    </div>
  )
}
