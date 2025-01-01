import { configureStore } from '@reduxjs/toolkit'
import userReducer from './features/user/userSlice'
import navigationReducer from './features/navigation/navigationSlice'

export const makeStore = () => {
  return configureStore({
    reducer: {
      user: userReducer,
      navigation: navigationReducer,
    }
  })
}

export type AppStore = ReturnType<typeof makeStore>
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']