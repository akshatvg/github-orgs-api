import axios from 'axios'

export function fetchRepos(){
  return{
    type:'FETCH_REPOS',
    payload:axios({
      method:'get',
      url:'https://cc-leaderboard.herokuapp.com/repos',
      headers:{
        'Access-Control-Allow-Origin':'*'
      }
    })
  }
}

export function fetchLeaderboard(){
  return{
    type:'FETCH_LEADERBOARD',
    payload:axios({
      method:'get',
      url:'https://cc-leaderboard.herokuapp.comleaderboard',
      headers:{
        'Access-Control-Allow-Origin':'*'
      }
    })
  }
}

