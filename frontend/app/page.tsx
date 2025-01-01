'use client'

import Link from 'next/link';
import Image from 'next/image';
import { useEffect, useState, useCallback } from 'react'
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {  Heart  } from 'lucide-react'
import { useAuth } from '@/components/ui/lib/useAuth';
import { PageList } from '@/components/pagelist';
import { useFetchWithHeaders } from '@/components/ui/lib/fetchWithHeaders';

function PostItem ({id, imageUrl, name, in_collection, collection_count}: {id:string, imageUrl: string, name:string, in_collection:boolean, collection_count:number}) {
  const [ heartColor, setHeartColor ] = useState("none")
  const [ count, setCount ] = useState(collection_count)
  const fetchWithHeaders = useFetchWithHeaders();
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/collections`;

  useEffect(() => {
    if (in_collection) {
        setHeartColor("#ef4444")
    } else {
        setHeartColor("none")
    }
  }, [in_collection])

  const fetchCollections = useCallback(async () => {
    if (heartColor === "#ef4444") {
        await fetchWithHeaders(`${url}/delete`, { method: 'DELETE',  headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ article_id: id }) })
        setHeartColor("none")
        setCount(count - 1)
    } else {
        await fetchWithHeaders(`${url}/add`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ article_id: id }) })
        setHeartColor("#ef4444")
        setCount(count + 1)
    }
  }, [heartColor, count, id, url, fetchWithHeaders])


  const handleClick = () => {
    fetchCollections();
  }
  
  
  return (
    <div className="relative group" key={id}>
      <Link href={`/posts/${id}`} className="absolute inset-0 z-10" prefetch={false}>
        <span className="sr-only">View</span>
      </Link>
      <Image
        src={imageUrl}
        alt="Apparel"
        width="400"
        height="300"
        className="rounded-lg object-cover w-full aspect-[4/3] group-hover:opacity-75 transition-opacity"
      />
      <div className="grid grid-cols-[auto_1fr] gap-2 p-4">
        <h3 className="font-semibold text-lg">{name}</h3>
        <Button variant="link" className="h-6 w-6 p-0 ml-auto z-20 grid grid-cols-[auto_1fr]" aria-label="Collect" onClick={handleClick}>
          <Heart className="h-6 w-6 stroke-0 hover:stroke-red-500 hover:stroke-2" style={{ fill: heartColor }} />
          {count > 0 && (<Badge variant="outline" className="ml-auto flex h-6 w-6 shrink-0 items-center justify-center">{count}</Badge>)}
        </Button>
      </div>
    </div>
  )
}

interface Post {
  id: string;
  imageUrl: string;
  name: string;
  in_collection: boolean;
  collection_count: number;
}

function usePosts(page: number, limit: number) {
  const [posts, setPosts] = useState<Post[]>([]);
  const fetchWithHeaders = useFetchWithHeaders();

  useEffect(() => {
    let isMounted = true;
    async function fetchPosts() {
      try {
        const offset = (page - 1) * limit;
        const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/posts/?limit=${limit}&offset=${offset}`;
        const data = await fetchWithHeaders(url);
        if (isMounted) {
          setPosts(data.posts);
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    }
    fetchPosts();
    return () => { isMounted = false; };
  }, [page, limit, fetchWithHeaders]);

  return { posts };
}

function useTotalPages(limit: number) {
  const [totalPages, setTotalPages] = useState(0);
  const fetchWithHeaders = useFetchWithHeaders();

  useEffect(() => {
    let isMounted = true;
    async function fetchTotalPages() {
      try {
        const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/posts/totalpages?limit=${limit}`;
        const data = await fetchWithHeaders(url);
        if (isMounted) {
          setTotalPages(data.totalPages);
        }
      } catch (error) {
        console.error('Error fetching total pages:', error);
      }
    }
    fetchTotalPages();
    return () => { isMounted = false; };
  }, [limit, fetchWithHeaders]);

  return { totalPages };
}

function RenderHome() {
  const [page, setPage] = useState(1)
  const limit = 6 //每次顯示6筆
  const { posts } = usePosts(page, limit)
  const { totalPages } = useTotalPages(limit)
  const pageWindowSize = 3 //每次顯示3個頁碼

  return (
    <section className="w-full py-5">
      <div className="container grid gap-6 md:gap-8 px-4 md:px-6 max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-8">
          <div className="grid gap-1">
            <h1 className="text-3xl font-bold tracking-tight">All LIMS Posts</h1>
            <p className="text-muted-foreground">Discover our past posts.</p>
          </div>
        </div>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
        {posts.map((post:Post) => (
            <PostItem key={post.id} {...post} />
          ))}

        </div>
      </div>
      <PageList totalPages={totalPages} page={page} setPage={setPage} pageWindowSize={pageWindowSize}/>
    </section>
  );
}
export default function Home() {
  const isLoggedIn = useAuth();
  if (!isLoggedIn) return null;
  return <RenderHome />;
}

