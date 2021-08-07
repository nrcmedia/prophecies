import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Task from '@/models/Task'

export default class TaskRecord extends Model {
  static entity = 'task-records'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      originalValue: this.string(),
      predictedValue: this.string(),
      link: this.string(),
      metadata: this.attr(null),
      rounds: this.number(),
      status: this.string(),
      task_id: this.attr(null),
      task: this.belongsTo(Task, 'task_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-records/`,
    dataTransformer: responseNormalizer
  }
}
