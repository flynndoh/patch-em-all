import mitt from 'mitt'
import events from '@/event-bus/events'
const EventBus = mitt()
export { EventBus, events }
