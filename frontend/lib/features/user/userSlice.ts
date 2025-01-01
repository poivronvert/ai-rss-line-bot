import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UserInfo {
  id: string
  name: string
  picture?: string | undefined
}

interface UserState {
  isLoggedIn: boolean
  userInfo: UserInfo | Record<string, never>
}

const initialState: UserState = {
  isLoggedIn: false,
  userInfo: {},
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    loginSuccess(state, action: PayloadAction<UserInfo>) {
      state.isLoggedIn = true
      state.userInfo = action.payload
    },
    logout: (state) => {
      state.isLoggedIn = false
      state.userInfo = initialState.userInfo
    },
  },
})

export const { loginSuccess, logout } = userSlice.actions

export default userSlice.reducer