import Layout from "./layouts"
import Head from 'next/head'
import Script from 'next/script'
import type { ReactElement}  from 'react'
import { useRouter } from "next/router"
import type { InferGetServerSidePropsType,GetServerSideProps} from 'next'
import { useState, useEffect } from 'react'
import api_urls from "../api_urls"
import moment from 'moment';

type Repo = {
  is_success: boolean,
  message: string,
  debug: object
}

type PostRecord = {
  title: string,
  descrip: string,
  created_at: string,
  tags: string,
  id: Number
}

export const getServerSideProps = (async () => {
  let post_url: string = `${process.env.NEXT_PUBLIC_API_URL}/${process.env.NEXT_PUBLIC_API_ROUTE}/${api_urls.url_get_posts}`
  if(process.env.Debug){
    console.log(post_url)
  }

  const resp = await fetch(post_url)
  if(process.env.Debug){
    console.log(resp)
  }
  const repo = await resp.json()

  return { props: { repo } }
  }) satisfies GetServerSideProps<{
    repo: Repo
  }>


const Home = ({ repo }:InferGetServerSidePropsType<typeof getServerSideProps>) => {
  const router = useRouter()

  let desc: string = "hello world2"

  let resp_header: ReactElement = <Head>
              <title>{process.env.NEXT_PUBLIC_API_URL}</title>
              <meta name="description" content={desc}/>
              </Head>

  if(repo.is_success){
    return (
      <>
        {resp_header}
        <div className="md:grid md:grid-cols-4 border-t">
        {
        repo = repo.data.map((data: PostRecord)=> {
            return (
              <div key="{data.id}" className="md:max-w-md rounded overflow-hidden shadow-lg py-3">
              <div className=" px-6 py-4 h-80">
                <div className="font-bold text-xl mb-2 uppercase">{data.title}</div>
                  <p className="text-gray-700 text-base">
                    {data.descrip.substring(0,400)}...
                  </p>
              </div>
              <div className="px-6 pt-4 pb-2">
              {data.tags && data.tags.split(",").map((content: string) => {return <span key={content.length} className="capitalize inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">{content}</span>})}
              </div>
              <div className="text-center mr-2 bg-gray-200 rounded-full p-2 mt-4 mb-3">Created at: {moment(data.created_at).toDate().toLocaleDateString()}</div>
              </div>

          )
        })
      }
      </div>

      </>
    )
  }else{
    {'something went wrong'}
  }
}

Home.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout data>
      {page}
    </Layout>
  )
}
export default Home