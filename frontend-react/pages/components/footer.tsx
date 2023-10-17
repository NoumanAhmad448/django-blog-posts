import moment from "moment"
import Image from "next/image"

const Footer = () => {
    return (
        <>
        <footer className="hero container max-w-screen-lg mx-auto py-10">
          <Image src="vercel.svg" alt="svg" width={600} height={600} className="mx-auto"/>
            <div className=" capitalize text-center p-4 mb-1 font-bold">
                all rights are reserved @ {moment().year()}
            </div>
        </footer>
        </>
    )
}

export default Footer