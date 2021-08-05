import { rest } from 'msw'

export default [
  rest.get('/api/v1/choice-groups', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        links: {
          first: 'http://localhost/api/v1/choice-groups/?page%5Bnumber%5D=1',
          last: 'http://localhost/api/v1/choice-groups/?page%5Bnumber%5D=1',
          next: null,
          prev: null
        },
        data: [
          {
            type: 'ChoiceGroup',
            id: '2',
            attributes: {
              name: 'Which pastry?'
            },
            relationships: {
              choices: {
                meta: {
                  count: 3
                },
                data: [
                  {
                    type: 'Choice',
                    id: '4'
                  },
                  {
                    type: 'Choice',
                    id: '5'
                  },
                  {
                    type: 'Choice',
                    id: '6'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/choice-groups/2/'
            }
          },
          {
            type: 'ChoiceGroup',
            id: '1',
            attributes: {
              name: 'Is it correct?'
            },
            relationships: {
              choices: {
                meta: {
                  count: 3
                },
                data: [
                  {
                    type: 'Choice',
                    id: '1'
                  },
                  {
                    type: 'Choice',
                    id: '2'
                  },
                  {
                    type: 'Choice',
                    id: '3'
                  }
                ]
              }
            },
            links: {
              self: 'http://localhost/api/v1/choice-groups/1/'
            }
          }
        ],
        included: [
          {
            type: 'Choice',
            id: '1',
            attributes: {
              name: 'Correct',
              value: 'correct',
              require_alternative_value: false
            }
          },
          {
            type: 'Choice',
            id: '2',
            attributes: {
              name: 'Incorrect',
              value: 'incorrect',
              require_alternative_value: false
            }
          },
          {
            type: 'Choice',
            id: '3',
            attributes: {
              name: 'Unkown',
              value: 'unkown',
              require_alternative_value: true
            }
          },
          {
            type: 'Choice',
            id: '4',
            attributes: {
              name: 'Babka',
              value: 'Babka',
              require_alternative_value: false
            }
          },
          {
            type: 'Choice',
            id: '5',
            attributes: {
              name: 'Croissant',
              value: 'Croissant',
              require_alternative_value: false
            }
          },
          {
            type: 'Choice',
            id: '6',
            attributes: {
              name: 'Muffin',
              value: 'Muffin',
              require_alternative_value: false
            }
          }
        ],
        meta: {
          pagination: {
            page: 1,
            pages: 1,
            count: 2
          }
        }
      })
    )
  }),

  rest.get('/api/v1/choice-groups/1', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          type: 'ChoiceGroup',
          id: '1',
          attributes: {
            name: 'Is it correct?'
          },
          relationships: {
            choices: {
              meta: {
                count: 3
              },
              data: [
                {
                  type: 'Choice',
                  id: '1'
                },
                {
                  type: 'Choice',
                  id: '2'
                },
                {
                  type: 'Choice',
                  id: '3'
                }
              ]
            }
          },
          links: {
            self: 'http://localhost/api/v1/choice-groups/1/'
          }
        },
        included: [
          {
            type: 'Choice',
            id: '1',
            attributes: {
              name: 'Correct',
              value: 'correct'
            }
          },
          {
            type: 'Choice',
            id: '2',
            attributes: {
              name: 'Incorrect',
              value: 'incorrect'
            }
          },
          {
            type: 'Choice',
            id: '3',
            attributes: {
              name: 'Unkown',
              value: 'unkown'
            }
          }
        ]
      })
    )
  }),

  rest.get('/api/v1/choice-groups/2', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          type: 'ChoiceGroup',
          id: '2',
          attributes: {
            name: 'Which pastry?'
          },
          relationships: {
            choices: {
              meta: {
                count: 3
              },
              data: [
                {
                  type: 'Choice',
                  id: '4'
                },
                {
                  type: 'Choice',
                  id: '5'
                },
                {
                  type: 'Choice',
                  id: '6'
                }
              ]
            }
          },
          links: {
            self: 'http://localhost/api/v1/choice-groups/2/'
          }
        },
        included: [
          {
            type: 'Choice',
            id: '4',
            attributes: {
              name: 'Babka',
              value: 'Babka'
            }
          },
          {
            type: 'Choice',
            id: '5',
            attributes: {
              name: 'Croissant',
              value: 'Croissant'
            }
          },
          {
            type: 'Choice',
            id: '6',
            attributes: {
              name: 'Muffin',
              value: 'Muffin'
            }
          }
        ]
      })
    )
  })
]
