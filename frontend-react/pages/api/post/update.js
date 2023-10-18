// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

const api_request =  (req, res) => {
  res.status(200).json({ name: 'John Doe' })
}

export default api_request