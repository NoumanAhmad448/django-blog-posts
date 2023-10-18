import type { NextApiRequest, NextApiResponse } from 'next'

const api_request =  (req:NextApiRequest, res: NextApiResponse) => {
    res.status(200).json({ name: 'John Doe' })
  }

export default api_request