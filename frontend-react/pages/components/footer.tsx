import moment from "moment"

const Footer = () => {
    return (
        <footer className="border border-blue-500 capitalize text-center p-4 mb-1 font-bold">all rights are reserved @ {moment().year()}</footer>
    )
}

export default Footer