import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface NavigationState {
  previousPageUrl: string;
}

export const initialState: NavigationState = {
  previousPageUrl: '/',
};

const navigationSlice = createSlice({
  name: 'navigation',
  initialState,
  reducers: {
    setPreviousPageUrl: (state, action: PayloadAction<string>) => {
      state.previousPageUrl = action.payload;
    },
  },
});

export const { setPreviousPageUrl } = navigationSlice.actions;
export default navigationSlice.reducer;