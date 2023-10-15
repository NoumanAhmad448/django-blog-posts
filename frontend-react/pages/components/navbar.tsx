import Link from 'next/link'

const Navbar = () => {
return (
  <ul className="flex p-5 border-b">
    <li className="mr-3">
      <Link
        className="text-lg font-bold inline-block border border-blue-500 rounded rounded-full py-1 px-3 bg-blue-500 text-white"
        href="/"
      >
        Blog Posts
      </Link>
    </li>
  </ul>
)
}

export default Navbar