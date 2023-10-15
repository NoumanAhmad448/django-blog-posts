import { useRouter } from 'next/router'

export function getAllPostIds() {
  const fileNames = fs.readdirSync(postsDirectory);
  return fileNames.map((fileName) => {
    return {
      params: {
        id: fileName.replace(/\.md$/, ''),
      },
    };
  });
}
export async function getServerSideProps(context) {
  return {
    props: {
      data: [{id: 1, name: "nouman"}]
    },
  };
}


const Home = ({ data }) => {
  const router = useRouter()
  console.log(data)
  return (
    <section>
      <div> Given post id {router.query.id} </div>
      <div> Given post id {router.query.name} </div>
      {
        data.map(data => {
          return <section key={data.id}><div> id: {data.id} </div><div> name: {data.name} </div>
                <button className="btn" onClick={() => router.push('/about')} type="button">hello next </button>
          </section>
        })
      }
    </section>
  )
}


export default Home