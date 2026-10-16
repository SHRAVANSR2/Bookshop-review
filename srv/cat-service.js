
const cds = require('@sap/cds')

module.exports = class CatalogService extends cds.ApplicationService {
  init() {
    const { Books, Reviews } = this.entities

    // Discount label on well-stocked books
    this.after('each', Books, book => {
      if (book.stock > 100) book.title += ' -- 11% off!'
    })

    // Validate review ratings before creation
    this.before('CREATE', Reviews, req => {
      const { rating } = req.data

      if (
        !Number.isInteger(rating) ||
        rating < 1 ||
        rating > 5
      ) {
        return req.reject(
          400,
          'Rating must be an integer between 1 and 5'
        )
      }
    })

    // Implement the custom action
    this.on('submitOrder', async req => {
      const { book, quantity } = req.data

      const n = await UPDATE(Books, book)
        .with`stock = stock - ${quantity}`
        .where`stock >= ${quantity}`

      if (!n) {
        return req.error(
          409,
          `${quantity} exceeds stock for book #${book}`
        )
      }
    })

    return super.init()
  }
}
