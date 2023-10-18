import type { NextApiRequest, NextApiResponse } from 'next'
const Joi = require("joi")

type response = {
  message: string|Array<string>,
  data: object
}

const schema = Joi.object({
  key: Joi.string()
      .min(3)
      .max(30)
      .required(),

  number: [
      Joi.number().required()
  ],
})

const api_request =  (req:NextApiRequest, res: NextApiResponse<response>) => {
    let response = {
      message: '',
      data: {
      }
    }
    if(req.method !== "POST"){
      response.message= "only post request is allowed"
      response.data = req.body

      res.status(405).json(response)
    }
    try{
      let data_validation = schema.validate(req.body)
      if(data_validation.error){
        response.message = data_validation.error.details
        res.status(412).json(response)
      }
      response.message= "data has been parsed and ready for action"
      response.data = data_validation.value
      res.status(200).json(response)
    }
    catch(error){
      response.message= "something went wrong"
      console.log(error)
      res.status(500).json(response)
    }
  }

export default api_request