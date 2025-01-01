'use client'

import  { useEffect, useState, useCallback } from 'react'
import Image from 'next/image'

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useAuth } from '@/components/ui/lib/useAuth'
import { useFetchWithHeaders } from '@/components/ui/lib/fetchWithHeaders';
import { Button } from '@/components/ui/button'

interface SectionProps {
    title: string;
    info: string;
    url: string[];
}

interface RenderPageProps {
    id: string;
}

type tParams = Promise<{ id: string }>

interface Post {
  title: string;
  engagement: string;
  public: string;
  regulation: string;
  innovation: string;
  deals: string;
  in_collection: boolean;
  links: {
    Engagement: string[];
    Public: string[];
    Regulation: string[];
    Innovation: string[];
    Deals: string[];
  };
}

const SectionTemplate = ({ title, info, url }: SectionProps) => {
    return (
        <main className="p-4">
            <div className="relative mb-8">
                <Image
                    src="/assets/robot.jpeg"
                    alt="Manufacturing facility"
                    width={800}
                    height={300}
                    className="w-full h-64 object-cover"
                />
            </div>

            <article className="mb-8">
                <h2 className="text-2xl font-bold mb-2">{title}</h2>
                <p className="text-gray-600 mb-4 whitespace-pre-line">{info}</p>
                {url && url.map((link, index) => (
                    <a
                        key={index}
                        href={link}
                        target='_blank'
                        className="bg-muted text-muted-foreground px-4 py-2 rounded mr-4"
                    >
                        瞭解更多
                    </a>
                    ))}
            </article>
        </main>
    );
};

function usePosts(id:string): { posts: Post | null } {
    const [posts, setPosts] = useState(null);
    const fetchWithHeaders = useFetchWithHeaders();

    useEffect(() => {
        async function fetchPosts() {
            const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/posts/${id}`
            const data = await fetchWithHeaders(url)
            setPosts(data)
        }
        fetchPosts()
    }, [fetchWithHeaders, id])
    return { posts }
}

export default function Page({ params }: { params: tParams }){
    const [id, setId] = useState<string>('')
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const auth = useAuth()

    useEffect(() => {
        async function init(){
            const { id } = await params
            setId(id)
            setIsLoggedIn(auth) 
        }
        init()
    }, [params, auth])

    if (!isLoggedIn) return null;

    return <RenderPage id={id}/>
}

const CollectionButton = ({ id, in_collection }: { id: string, in_collection: boolean }) => {
    const [isCollected, setIsCollected] = useState(in_collection);
    const fetchWithHeaders = useFetchWithHeaders();
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/collections`;

    const fetchCollections = useCallback(async () => {
        if (isCollected) {
            console.log('delete')
            await fetchWithHeaders(`${url}/delete`, { method: 'DELETE',  headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ article_id: id }) })
            setIsCollected(false)
        } else {
            console.log('add')
            await fetchWithHeaders(`${url}/add`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ article_id: id }) })
            setIsCollected(true);
        }
      }, [isCollected, id, url, fetchWithHeaders])
      
      const handleClick = () => {
        fetchCollections();
      };

    return (
        <Button variant="outline" onClick={handleClick}>{isCollected ? '已收藏' : '收藏'}</Button>
    )
}

function RenderPage({id}: RenderPageProps) {
    const { posts } = usePosts(id)
    if (!posts) return null
    const date = posts.title?.split(" ")
    const { links } = posts
    const { Engagement, Public, Regulation, Innovation, Deals } = links ?? {};
    console.log(posts)


    return (
        <div className="max-w-auto mx-auto bg-white shadow-lg">
            <header className="p-4 border-b">
                <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                        <Avatar>
                            <AvatarImage
                                src="/assets/robot.jpeg"
                                alt="Robot"
                            />
                            <AvatarFallback>R</AvatarFallback>
                        </Avatar>
                        <span className="text-xl font-semibold">Daily Digest</span>
                    </div>
                    <div className="flex items-center space-x-6">
                        <span className="text-gray-500">{date}</span>
                        <CollectionButton id={id} in_collection={posts.in_collection}/>
                    </div>
                </div>
            </header>

            {posts.engagement!== "" && <SectionTemplate title="Engagement" info={posts.engagement} url={Engagement}/>}
            {posts.public!== "" && <SectionTemplate title="Public" info={posts.public} url={Public}/>}
            {posts.regulation!== "" && <SectionTemplate title="Regulation" info={posts.regulation} url={Regulation}/>}
            {posts.innovation!== "" && <SectionTemplate title="Innovation" info={posts.innovation} url={Innovation}/>}
            {posts.deals!== "" && <SectionTemplate title="Deals" info={posts.deals} url={Deals}/>}

            <footer className="bg-gray-200 p-4 text-center text-sm text-gray-600">
                <p>Copyright© 2024</p>
            </footer>
        </div>
    )
}
